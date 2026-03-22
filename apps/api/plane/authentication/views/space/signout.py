# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

# Python imports
import os
from urllib.parse import urlencode

# Django imports
from django.views import View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.utils import timezone

# Module imports
from plane.authentication.utils.host import base_host, user_ip
from plane.db.models import User, Account
from plane.license.utils.instance_value import get_configuration_value
from plane.utils.path_validator import get_safe_redirect_url


class SignOutAuthSpaceEndpoint(View):
    def post(self, request):
        next_path = request.POST.get("next_path")

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

            # Log the user out of Django
            logout(request)

            # Redirect to Zitadel end-session endpoint
            space_base_url = base_host(request=request, is_space=True)
            (ZITADEL_ISSUER_URL,) = get_configuration_value(
                [
                    {
                        "key": "ZITADEL_ISSUER_URL",
                        "default": os.environ.get("ZITADEL_ISSUER_URL", ""),
                    },
                ]
            )

            if ZITADEL_ISSUER_URL and id_token:
                post_logout_uri = get_safe_redirect_url(base_url=space_base_url, next_path=next_path)
                params = {
                    "id_token_hint": id_token,
                    "post_logout_redirect_uri": post_logout_uri,
                }
                end_session_url = f"{ZITADEL_ISSUER_URL.rstrip('/')}/oidc/v1/end_session?{urlencode(params)}"
                return HttpResponseRedirect(end_session_url)

            url = get_safe_redirect_url(base_url=space_base_url, next_path=next_path)
            return HttpResponseRedirect(url)
        except Exception:
            url = get_safe_redirect_url(
                base_url=base_host(request=request, is_space=True),
                next_path=next_path,
            )
            return HttpResponseRedirect(url)
