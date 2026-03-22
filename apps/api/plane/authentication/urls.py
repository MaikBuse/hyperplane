# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

from django.urls import path

from .views import (
    CSRFTokenEndpoint,
    ChangePasswordEndpoint,
    SetUserPasswordEndpoint,
    ForgotPasswordEndpoint,
    ResetPasswordEndpoint,
    # App
    EmailCheckEndpoint,
    MagicGenerateEndpoint,
    MagicSignInEndpoint,
    MagicSignUpEndpoint,
    SignInAuthEndpoint,
    SignOutAuthEndpoint,
    SignUpAuthEndpoint,
    ZitadelOIDCInitiateEndpoint,
    ZitadelOIDCCallbackEndpoint,
    # Space
    EmailCheckSpaceEndpoint,
    ForgotPasswordSpaceEndpoint,
    ResetPasswordSpaceEndpoint,
    MagicGenerateSpaceEndpoint,
    MagicSignInSpaceEndpoint,
    MagicSignUpSpaceEndpoint,
    SignInAuthSpaceEndpoint,
    SignUpAuthSpaceEndpoint,
    SignOutAuthSpaceEndpoint,
    ZitadelOIDCInitiateSpaceEndpoint,
    ZitadelOIDCCallbackSpaceEndpoint,
)

urlpatterns = [
    # Email/password credentials
    path("sign-in/", SignInAuthEndpoint.as_view(), name="sign-in"),
    path("sign-up/", SignUpAuthEndpoint.as_view(), name="sign-up"),
    path("spaces/sign-in/", SignInAuthSpaceEndpoint.as_view(), name="space-sign-in"),
    path("spaces/sign-up/", SignUpAuthSpaceEndpoint.as_view(), name="space-sign-up"),
    # Sign out
    path("sign-out/", SignOutAuthEndpoint.as_view(), name="sign-out"),
    path("spaces/sign-out/", SignOutAuthSpaceEndpoint.as_view(), name="space-sign-out"),
    # CSRF token
    path("get-csrf-token/", CSRFTokenEndpoint.as_view(), name="get_csrf_token"),
    # Magic sign in
    path("magic-generate/", MagicGenerateEndpoint.as_view(), name="magic-generate"),
    path("magic-sign-in/", MagicSignInEndpoint.as_view(), name="magic-sign-in"),
    path("magic-sign-up/", MagicSignUpEndpoint.as_view(), name="magic-sign-up"),
    path("spaces/magic-generate/", MagicGenerateSpaceEndpoint.as_view(), name="space-magic-generate"),
    path("spaces/magic-sign-in/", MagicSignInSpaceEndpoint.as_view(), name="space-magic-sign-in"),
    path("spaces/magic-sign-up/", MagicSignUpSpaceEndpoint.as_view(), name="space-magic-sign-up"),
    # Email Check
    path("email-check/", EmailCheckEndpoint.as_view(), name="email-check"),
    path("spaces/email-check/", EmailCheckSpaceEndpoint.as_view(), name="space-email-check"),
    # Password management
    path("forgot-password/", ForgotPasswordEndpoint.as_view(), name="forgot-password"),
    path("reset-password/<uidb64>/<token>/", ResetPasswordEndpoint.as_view(), name="reset-password"),
    path("spaces/forgot-password/", ForgotPasswordSpaceEndpoint.as_view(), name="space-forgot-password"),
    path("spaces/reset-password/<uidb64>/<token>/", ResetPasswordSpaceEndpoint.as_view(), name="space-reset-password"),
    path("change-password/", ChangePasswordEndpoint.as_view(), name="change-password"),
    path("set-password/", SetUserPasswordEndpoint.as_view(), name="set-password"),
    # Zitadel OIDC
    path("zitadel/", ZitadelOIDCInitiateEndpoint.as_view(), name="zitadel-initiate"),
    path("zitadel/callback/", ZitadelOIDCCallbackEndpoint.as_view(), name="zitadel-callback"),
    path("spaces/zitadel/", ZitadelOIDCInitiateSpaceEndpoint.as_view(), name="space-zitadel-initiate"),
    path("spaces/zitadel/callback/", ZitadelOIDCCallbackSpaceEndpoint.as_view(), name="space-zitadel-callback"),
]
