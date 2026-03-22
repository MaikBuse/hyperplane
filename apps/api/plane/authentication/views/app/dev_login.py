# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

"""
Dev-only login endpoint. Bypasses Zitadel OIDC by creating/fetching a local
dev user and establishing a Django session. Only available when DEBUG=True.

Usage: visit http://localhost:8000/auth/dev-login/ in your browser.
"""

import logging
import uuid

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views import View

from plane.authentication.utils.host import base_host
from plane.authentication.utils.login import user_login
from plane.authentication.utils.redirection_path import get_redirection_path
from plane.authentication.utils.user_auth_workflow import post_user_auth_workflow
from plane.db.models import User
from plane.license.models import Instance

logger = logging.getLogger("plane.authentication")

DEV_USER_EMAIL = "dev@hyperplane.local"


class DevLoginEndpoint(View):
    """Instant login for local development — no Zitadel required."""

    def get(self, request):
        if not settings.DEBUG:
            return HttpResponseForbidden("Dev login is only available in DEBUG mode.")

        # Ensure the instance is set up
        instance = Instance.objects.first()
        if instance is None:
            Instance.objects.create(
                instance_name="Local Development",
                instance_id=uuid.uuid4().hex,
                current_version="0.0.0-dev",
                last_checked_at=timezone.now(),
                is_setup_done=True,
            )

        # Get or create the dev user
        user, created = User.objects.get_or_create(
            email=DEV_USER_EMAIL,
            defaults={
                "username": "dev",
                "first_name": "Dev",
                "last_name": "User",
                "display_name": "Dev User",
                "is_active": True,
                "is_email_verified": True,
                "is_password_autoset": True,
            },
        )

        if created:
            user.set_unusable_password()
            user.save()
            logger.info("Created dev user: %s", DEV_USER_EMAIL)

        # Run the standard post-auth workflow (creates Profile, etc.)
        post_user_auth_workflow(
            user=user,
            is_signup=created,
            request=request,
        )

        # Establish session
        user_login(request=request, user=user, is_app=True)

        # Redirect to the app
        next_path = request.GET.get("next_path") or get_redirection_path(user=user)
        host = base_host(request=request, is_app=True)
        return HttpResponseRedirect(f"{host}/{next_path}")
