# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

# Python imports
import os
import uuid
from urllib.parse import urlencode, urljoin

# Django imports
from django.http import HttpResponseRedirect
from django.views import View
from django.utils import timezone
from django.contrib.auth import logout

# Third party imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Module imports
from .base import BaseAPIView
from plane.license.api.permissions import InstanceAdminPermission
from plane.license.api.serializers import (
    InstanceAdminMeSerializer,
    InstanceAdminSerializer,
)
from plane.license.models import Instance, InstanceAdmin
from plane.db.models import User, Account
from plane.utils.cache import cache_response, invalidate_cache
from plane.authentication.utils.login import user_login
from plane.authentication.utils.host import base_host, user_ip
from plane.authentication.adapter.error import (
    AUTHENTICATION_ERROR_CODES,
    AuthenticationException,
)
from plane.authentication.provider.oidc.zitadel import ZitadelOIDCProvider
from plane.authentication.utils.user_auth_workflow import post_user_auth_workflow
from plane.utils.ip_address import get_client_ip
from plane.utils.path_validator import get_safe_redirect_url
from plane.license.utils.instance_value import get_configuration_value


class InstanceAdminEndpoint(BaseAPIView):
    permission_classes = [InstanceAdminPermission]

    @invalidate_cache(path="/api/instances/", user=False)
    # Create an instance admin
    def post(self, request):
        email = request.data.get("email", False)
        role = request.data.get("role", 20)

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        instance = Instance.objects.first()
        if instance is None:
            return Response(
                {"error": "Instance is not registered yet"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Fetch the user
        user = User.objects.get(email=email)

        instance_admin = InstanceAdmin.objects.create(instance=instance, user=user, role=role)
        serializer = InstanceAdminSerializer(instance_admin)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @cache_response(60 * 60 * 2, user=False)
    def get(self, request):
        instance = Instance.objects.first()
        if instance is None:
            return Response(
                {"error": "Instance is not registered yet"},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance_admins = InstanceAdmin.objects.filter(instance=instance)
        serializer = InstanceAdminSerializer(instance_admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @invalidate_cache(path="/api/instances/", user=False)
    def delete(self, request, pk):
        instance = Instance.objects.first()
        InstanceAdmin.objects.filter(instance=instance, pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InstanceAdminSignUpEndpoint(View):
    """Redirects to Zitadel OIDC for initial admin setup."""

    permission_classes = [AllowAny]

    def get(self, request):
        instance = Instance.objects.first()
        if instance is None:
            exc = AuthenticationException(
                error_code=AUTHENTICATION_ERROR_CODES["INSTANCE_NOT_CONFIGURED"],
                error_message="INSTANCE_NOT_CONFIGURED",
            )
            url = urljoin(
                base_host(request=request, is_admin=True),
                "?" + urlencode(exc.get_error_dict()),
            )
            return HttpResponseRedirect(url)

        if InstanceAdmin.objects.first():
            exc = AuthenticationException(
                error_code=AUTHENTICATION_ERROR_CODES["ADMIN_ALREADY_EXIST"],
                error_message="ADMIN_ALREADY_EXIST",
            )
            url = urljoin(
                base_host(request=request, is_admin=True),
                "?" + urlencode(exc.get_error_dict()),
            )
            return HttpResponseRedirect(url)

        try:
            state = uuid.uuid4().hex
            admin_redirect_uri = (
                f"{'https' if request.is_secure() else 'http'}://"
                f"{request.get_host()}/api/instances/admins/oidc/callback/"
            )
            provider = ZitadelOIDCProvider(request=request, state=state, redirect_uri=admin_redirect_uri)
            request.session["state"] = state
            request.session["admin_setup"] = True
            auth_url = provider.get_auth_url()
            return HttpResponseRedirect(auth_url)
        except AuthenticationException as e:
            params = e.get_error_dict()
            url = urljoin(
                base_host(request=request, is_admin=True),
                "?" + urlencode(params),
            )
            return HttpResponseRedirect(url)


class InstanceAdminSignInEndpoint(View):
    """Redirects to Zitadel OIDC for admin sign-in."""

    permission_classes = [AllowAny]

    def get(self, request):
        instance = Instance.objects.first()
        if instance is None:
            exc = AuthenticationException(
                error_code=AUTHENTICATION_ERROR_CODES["INSTANCE_NOT_CONFIGURED"],
                error_message="INSTANCE_NOT_CONFIGURED",
            )
            url = urljoin(
                base_host(request=request, is_admin=True),
                "?" + urlencode(exc.get_error_dict()),
            )
            return HttpResponseRedirect(url)

        try:
            state = uuid.uuid4().hex
            admin_redirect_uri = (
                f"{'https' if request.is_secure() else 'http'}://"
                f"{request.get_host()}/api/instances/admins/oidc/callback/"
            )
            provider = ZitadelOIDCProvider(request=request, state=state, redirect_uri=admin_redirect_uri)
            request.session["state"] = state
            request.session["admin_sign_in"] = True
            auth_url = provider.get_auth_url()
            return HttpResponseRedirect(auth_url)
        except AuthenticationException as e:
            params = e.get_error_dict()
            url = urljoin(
                base_host(request=request, is_admin=True),
                "?" + urlencode(params),
            )
            return HttpResponseRedirect(url)


class InstanceAdminOIDCCallbackEndpoint(View):
    """Handles Zitadel OIDC callback for admin sign-in and setup."""

    permission_classes = [AllowAny]

    @invalidate_cache(path="/api/instances/", user=False)
    def get(self, request):
        code = request.GET.get("code")
        state = request.GET.get("state")
        is_setup = request.session.pop("admin_setup", False)
        request.session.pop("admin_sign_in", None)

        if state != request.session.get("state", ""):
            exc = AuthenticationException(
                error_code=AUTHENTICATION_ERROR_CODES["ZITADEL_OIDC_PROVIDER_ERROR"],
                error_message="ZITADEL_OIDC_PROVIDER_ERROR",
            )
            url = urljoin(
                base_host(request=request, is_admin=True),
                "?" + urlencode(exc.get_error_dict()),
            )
            return HttpResponseRedirect(url)

        if not code:
            exc = AuthenticationException(
                error_code=AUTHENTICATION_ERROR_CODES["ZITADEL_OIDC_PROVIDER_ERROR"],
                error_message="ZITADEL_OIDC_PROVIDER_ERROR",
            )
            url = urljoin(
                base_host(request=request, is_admin=True),
                "?" + urlencode(exc.get_error_dict()),
            )
            return HttpResponseRedirect(url)

        try:
            admin_redirect_uri = (
                f"{'https' if request.is_secure() else 'http'}://"
                f"{request.get_host()}/api/instances/admins/oidc/callback/"
            )
            provider = ZitadelOIDCProvider(
                request=request,
                code=code,
                callback=post_user_auth_workflow,
                redirect_uri=admin_redirect_uri,
            )
            user = provider.authenticate()

            instance = Instance.objects.first()

            if is_setup and not InstanceAdmin.objects.exists():
                # First admin setup — register user as instance admin
                InstanceAdmin.objects.create(user=user, instance=instance)
                instance.is_setup_done = True
                instance.save()
            else:
                # Normal admin sign-in — verify user is an instance admin
                if not InstanceAdmin.objects.filter(instance=instance, user=user).exists():
                    exc = AuthenticationException(
                        error_code=AUTHENTICATION_ERROR_CODES["ADMIN_AUTHENTICATION_FAILED"],
                        error_message="ADMIN_AUTHENTICATION_FAILED",
                    )
                    url = urljoin(
                        base_host(request=request, is_admin=True),
                        "?" + urlencode(exc.get_error_dict()),
                    )
                    return HttpResponseRedirect(url)

            # Update user activity
            user.is_active = True
            user.last_active = timezone.now()
            user.last_login_time = timezone.now()
            user.last_login_ip = get_client_ip(request=request)
            user.last_login_uagent = request.META.get("HTTP_USER_AGENT")
            user.token_updated_at = timezone.now()
            user.save()

            user_login(request=request, user=user, is_admin=True)
            url = urljoin(base_host(request=request, is_admin=True), "general/")
            return HttpResponseRedirect(url)
        except AuthenticationException as e:
            params = e.get_error_dict()
            url = urljoin(
                base_host(request=request, is_admin=True),
                "?" + urlencode(params),
            )
            return HttpResponseRedirect(url)


class InstanceAdminUserMeEndpoint(BaseAPIView):
    permission_classes = [InstanceAdminPermission]

    def get(self, request):
        serializer = InstanceAdminMeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InstanceAdminUserSessionEndpoint(BaseAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated and InstanceAdmin.objects.filter(user=request.user).exists():
            serializer = InstanceAdminMeSerializer(request.user)
            data = {"is_authenticated": True}
            data["user"] = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"is_authenticated": False}, status=status.HTTP_200_OK)


class InstanceAdminSignOutEndpoint(View):
    permission_classes = [InstanceAdminPermission]

    def post(self, request):
        # Get user
        try:
            user = User.objects.get(pk=request.user.id)
            user.last_logout_ip = user_ip(request=request)
            user.last_logout_time = timezone.now()
            user.save()

            # Get id_token for Zitadel end-session
            id_token = ""
            account = Account.objects.filter(user=user, provider="zitadel").first()
            if account:
                id_token = account.id_token

            # Log the user out
            logout(request)

            # Redirect to Zitadel end-session endpoint
            admin_base_url = base_host(request=request, is_admin=True)
            (ZITADEL_ISSUER_URL,) = get_configuration_value(
                [
                    {
                        "key": "ZITADEL_ISSUER_URL",
                        "default": os.environ.get("ZITADEL_ISSUER_URL", ""),
                    },
                ]
            )

            if ZITADEL_ISSUER_URL and id_token:
                from urllib.parse import urlencode as _urlencode

                params = {
                    "id_token_hint": id_token,
                    "post_logout_redirect_uri": admin_base_url,
                }
                end_session_url = f"{ZITADEL_ISSUER_URL.rstrip('/')}/oidc/v1/end_session?{_urlencode(params)}"
                return HttpResponseRedirect(end_session_url)

            url = get_safe_redirect_url(base_url=admin_base_url, next_path="")
            return HttpResponseRedirect(url)
        except Exception:
            url = get_safe_redirect_url(base_url=base_host(request=request, is_admin=True), next_path="")
            return HttpResponseRedirect(url)
