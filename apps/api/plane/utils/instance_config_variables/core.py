# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

# Python imports
import os

authentication_config_variables = [
    {
        "key": "ENABLE_SIGNUP",
        "value": os.environ.get("ENABLE_SIGNUP", "1"),
        "category": "AUTHENTICATION",
        "is_encrypted": False,
    },
]

workspace_management_config_variables = [
    {
        "key": "DISABLE_WORKSPACE_CREATION",
        "value": os.environ.get("DISABLE_WORKSPACE_CREATION", "0"),
        "category": "WORKSPACE_MANAGEMENT",
        "is_encrypted": False,
    },
]

zitadel_config_variables = [
    {
        "key": "ZITADEL_ISSUER_URL",
        "value": os.environ.get("ZITADEL_ISSUER_URL", ""),
        "category": "ZITADEL",
        "is_encrypted": False,
    },
    {
        "key": "ZITADEL_CLIENT_ID",
        "value": os.environ.get("ZITADEL_CLIENT_ID", ""),
        "category": "ZITADEL",
        "is_encrypted": False,
    },
    {
        "key": "ZITADEL_CLIENT_SECRET",
        "value": os.environ.get("ZITADEL_CLIENT_SECRET", ""),
        "category": "ZITADEL",
        "is_encrypted": True,
    },
]

smtp_config_variables = [
    {
        "key": "ENABLE_SMTP",
        "value": os.environ.get("ENABLE_SMTP", "0"),
        "category": "SMTP",
        "is_encrypted": False,
    },
    {
        "key": "EMAIL_HOST",
        "value": os.environ.get("EMAIL_HOST", ""),
        "category": "SMTP",
        "is_encrypted": False,
    },
    {
        "key": "EMAIL_HOST_USER",
        "value": os.environ.get("EMAIL_HOST_USER", ""),
        "category": "SMTP",
        "is_encrypted": False,
    },
    {
        "key": "EMAIL_HOST_PASSWORD",
        "value": os.environ.get("EMAIL_HOST_PASSWORD", ""),
        "category": "SMTP",
        "is_encrypted": True,
    },
    {
        "key": "EMAIL_PORT",
        "value": os.environ.get("EMAIL_PORT", "587"),
        "category": "SMTP",
        "is_encrypted": False,
    },
    {
        "key": "EMAIL_FROM",
        "value": os.environ.get("EMAIL_FROM", ""),
        "category": "SMTP",
        "is_encrypted": False,
    },
    {
        "key": "EMAIL_USE_TLS",
        "value": os.environ.get("EMAIL_USE_TLS", "1"),
        "category": "SMTP",
        "is_encrypted": False,
    },
    {
        "key": "EMAIL_USE_SSL",
        "value": os.environ.get("EMAIL_USE_SSL", "0"),
        "category": "SMTP",
        "is_encrypted": False,
    },
]

llm_config_variables = [
    {
        "key": "LLM_API_KEY",
        "value": os.environ.get("LLM_API_KEY"),
        "category": "AI",
        "is_encrypted": True,
    },
    {
        "key": "LLM_PROVIDER",
        "value": os.environ.get("LLM_PROVIDER", "openai"),
        "category": "AI",
        "is_encrypted": False,
    },
    {
        "key": "LLM_MODEL",
        "value": os.environ.get("LLM_MODEL", "gpt-4o-mini"),
        "category": "AI",
        "is_encrypted": False,
    },
    # Deprecated, use LLM_MODEL
    {
        "key": "GPT_ENGINE",
        "value": os.environ.get("GPT_ENGINE", "gpt-3.5-turbo"),
        "category": "AI",
        "is_encrypted": False,
    },
]

unsplash_config_variables = [
    {
        "key": "UNSPLASH_ACCESS_KEY",
        "value": os.environ.get("UNSPLASH_ACCESS_KEY", ""),
        "category": "UNSPLASH",
        "is_encrypted": True,
    },
]

intercom_config_variables = [
    {
        "key": "IS_INTERCOM_ENABLED",
        "value": os.environ.get("IS_INTERCOM_ENABLED", "1"),
        "category": "INTERCOM",
        "is_encrypted": False,
    },
    {
        "key": "INTERCOM_APP_ID",
        "value": os.environ.get("INTERCOM_APP_ID", ""),
        "category": "INTERCOM",
        "is_encrypted": False,
    },
]

core_config_variables = [
    *authentication_config_variables,
    *workspace_management_config_variables,
    *zitadel_config_variables,
    *smtp_config_variables,
    *llm_config_variables,
    *unsplash_config_variables,
    *intercom_config_variables,
]
