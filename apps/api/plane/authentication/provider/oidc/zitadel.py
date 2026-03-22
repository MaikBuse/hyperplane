# Python imports
import os
from datetime import datetime, timedelta
from urllib.parse import urlencode

import pytz
import requests

# Module imports
from plane.authentication.adapter.oauth import OauthAdapter
from plane.license.utils.instance_value import get_configuration_value
from plane.authentication.adapter.error import (
    AUTHENTICATION_ERROR_CODES,
    AuthenticationException,
)


class ZitadelOIDCProvider(OauthAdapter):
    provider = "zitadel"

    def __init__(self, request, code=None, state=None, callback=None, redirect_uri=None):
        (ZITADEL_ISSUER_URL, ZITADEL_CLIENT_ID, ZITADEL_CLIENT_SECRET) = (
            get_configuration_value(
                [
                    {
                        "key": "ZITADEL_ISSUER_URL",
                        "default": os.environ.get("ZITADEL_ISSUER_URL"),
                    },
                    {
                        "key": "ZITADEL_CLIENT_ID",
                        "default": os.environ.get("ZITADEL_CLIENT_ID"),
                    },
                    {
                        "key": "ZITADEL_CLIENT_SECRET",
                        "default": os.environ.get("ZITADEL_CLIENT_SECRET"),
                    },
                ]
            )
        )

        if not (ZITADEL_ISSUER_URL and ZITADEL_CLIENT_ID and ZITADEL_CLIENT_SECRET):
            raise AuthenticationException(
                error_code=AUTHENTICATION_ERROR_CODES["ZITADEL_NOT_CONFIGURED"],
                error_message="ZITADEL_NOT_CONFIGURED",
            )

        self.issuer_url = ZITADEL_ISSUER_URL.rstrip("/")
        client_id = ZITADEL_CLIENT_ID
        client_secret = ZITADEL_CLIENT_SECRET

        # Discover OIDC endpoints
        oidc_config = self._discover_endpoints(self.issuer_url)

        scope = "openid email profile"
        if not redirect_uri:
            redirect_uri = (
                f'{"https" if request.is_secure() else "http"}://'
                f"{request.get_host()}/auth/zitadel/callback/"
            )

        url_params = {
            "client_id": client_id,
            "scope": scope,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
        }
        auth_url = (
            f"{oidc_config['authorization_endpoint']}?{urlencode(url_params)}"
        )

        token_url = oidc_config["token_endpoint"]
        userinfo_url = oidc_config["userinfo_endpoint"]
        self.end_session_endpoint = oidc_config.get("end_session_endpoint", "")

        super().__init__(
            request,
            self.provider,
            client_id,
            scope,
            redirect_uri,
            auth_url,
            token_url,
            userinfo_url,
            client_secret,
            code,
            callback=callback,
        )

    @staticmethod
    def _discover_endpoints(issuer_url):
        """Fetch OIDC discovery document."""
        discovery_url = f"{issuer_url}/.well-known/openid-configuration"
        try:
            response = requests.get(discovery_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            raise AuthenticationException(
                error_code=AUTHENTICATION_ERROR_CODES[
                    "ZITADEL_OIDC_PROVIDER_ERROR"
                ],
                error_message="ZITADEL_OIDC_PROVIDER_ERROR",
            )

    def set_token_data(self):
        data = {
            "code": self.code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        token_response = self.get_user_token(data=data)

        expires_in = token_response.get("expires_in")
        super().set_token_data(
            {
                "access_token": token_response.get("access_token"),
                "refresh_token": token_response.get("refresh_token", None),
                "access_token_expired_at": (
                    datetime.now(tz=pytz.utc) + timedelta(seconds=expires_in)
                    if expires_in
                    else None
                ),
                "refresh_token_expired_at": None,
                "id_token": token_response.get("id_token", ""),
            }
        )

    def set_user_data(self):
        user_info_response = self.get_user_response()
        user_data = {
            "email": user_info_response.get("email"),
            "user": {
                "avatar": user_info_response.get("picture", ""),
                "first_name": user_info_response.get("given_name", ""),
                "last_name": user_info_response.get("family_name", ""),
                "provider_id": user_info_response.get("sub"),
                "is_password_autoset": True,
            },
        }
        super().set_user_data(user_data)
