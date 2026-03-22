# Generated migration to add 'zitadel' to Account.PROVIDER_CHOICES

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0120_issueview_archived_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="provider",
            field=models.CharField(
                choices=[
                    ("google", "Google"),
                    ("github", "Github"),
                    ("gitlab", "GitLab"),
                    ("zitadel", "Zitadel"),
                ]
            ),
        ),
    ]
