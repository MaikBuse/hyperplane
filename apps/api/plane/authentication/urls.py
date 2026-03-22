# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from django.urls import path

from .views import (
    CSRFTokenEndpoint,
    DevLoginEndpoint,
    ZitadelOIDCInitiateEndpoint,
    ZitadelOIDCCallbackEndpoint,
    ZitadelOIDCInitiateSpaceEndpoint,
    ZitadelOIDCCallbackSpaceEndpoint,
    SignOutAuthEndpoint,
    SignOutAuthSpaceEndpoint,
)

urlpatterns = [
    # Zitadel OIDC
    path("zitadel/", ZitadelOIDCInitiateEndpoint.as_view(), name="zitadel-initiate"),
    path("zitadel/callback/", ZitadelOIDCCallbackEndpoint.as_view(), name="zitadel-callback"),
    path("spaces/zitadel/", ZitadelOIDCInitiateSpaceEndpoint.as_view(), name="space-zitadel-initiate"),
    path("spaces/zitadel/callback/", ZitadelOIDCCallbackSpaceEndpoint.as_view(), name="space-zitadel-callback"),
    # Dev login (DEBUG only)
    path("dev-login/", DevLoginEndpoint.as_view(), name="dev-login"),
    # Sign out
    path("sign-out/", SignOutAuthEndpoint.as_view(), name="sign-out"),
    path("spaces/sign-out/", SignOutAuthSpaceEndpoint.as_view(), name="space-sign-out"),
    # CSRF token
    path("get-csrf-token/", CSRFTokenEndpoint.as_view(), name="get_csrf_token"),
]
