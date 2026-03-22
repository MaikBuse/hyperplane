# Copyright (c) 2023-present Plane Software, Inc. and contributors
# SPDX-License-Identifier: AGPL-3.0-only
# See the LICENSE file for details.

# Python imports
import os

# Django imports
from django.core.management.base import BaseCommand, CommandError

# Module imports
from plane.license.models import InstanceConfiguration
from plane.utils.instance_config_variables import instance_config_variables


class Command(BaseCommand):
    help = "Configure instance variables"

    def handle(self, *args, **options):
        from plane.license.utils.encryption import encrypt_data
        from plane.license.utils.instance_value import get_configuration_value

        mandatory_keys = ["SECRET_KEY"]

        for item in mandatory_keys:
            if not os.environ.get(item):
                raise CommandError(f"{item} env variable is required.")

        for item in instance_config_variables:
            obj, created = InstanceConfiguration.objects.get_or_create(key=item.get("key"))
            if created:
                obj.category = item.get("category")
                obj.is_encrypted = item.get("is_encrypted", False)
                if item.get("is_encrypted", False):
                    obj.value = encrypt_data(item.get("value"))
                else:
                    obj.value = item.get("value")
                obj.save()
                self.stdout.write(self.style.SUCCESS(f"{obj.key} loaded with value from environment variable."))
            else:
                self.stdout.write(self.style.WARNING(f"{obj.key} configuration already exists"))

        # Check if Zitadel is configured
        key = "IS_ZITADEL_ENABLED"
        if not InstanceConfiguration.objects.filter(key=key).exists():
            ZITADEL_ISSUER_URL, ZITADEL_CLIENT_ID, ZITADEL_CLIENT_SECRET = get_configuration_value(
                [
                    {
                        "key": "ZITADEL_ISSUER_URL",
                        "default": os.environ.get("ZITADEL_ISSUER_URL", ""),
                    },
                    {
                        "key": "ZITADEL_CLIENT_ID",
                        "default": os.environ.get("ZITADEL_CLIENT_ID", ""),
                    },
                    {
                        "key": "ZITADEL_CLIENT_SECRET",
                        "default": os.environ.get("ZITADEL_CLIENT_SECRET", ""),
                    },
                ]
            )
            value = "1" if (ZITADEL_ISSUER_URL and ZITADEL_CLIENT_ID and ZITADEL_CLIENT_SECRET) else "0"
            InstanceConfiguration.objects.create(
                key=key,
                value=value,
                category="AUTHENTICATION",
                is_encrypted=False,
            )
            self.stdout.write(self.style.SUCCESS(f"{key} loaded with value from environment variable."))
        else:
            self.stdout.write(self.style.WARNING(f"{key} configuration already exists"))
