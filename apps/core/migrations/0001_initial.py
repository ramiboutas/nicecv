# Generated by Django 4.1.7 on 2023-06-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=8, unique=True)),
                ("name", models.CharField(default="Other Language", max_length=32)),
                ("available_in_deepl", models.BooleanField(default=False)),
                (
                    "deepl_formality",
                    models.BooleanField(
                        default=False, verbose_name="Support formality on Deepl"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Setting",
            fields=[
                (
                    "singleton",
                    models.BooleanField(
                        default=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="API keys and dynamic settings", max_length=32
                    ),
                ),
                ("linkedin_client_id", models.CharField(blank=True, max_length=255)),
                (
                    "linkedin_client_secret",
                    models.CharField(blank=True, max_length=255),
                ),
                ("linkedin_profile_id", models.CharField(blank=True, max_length=255)),
                ("linkedin_access_token", models.CharField(blank=True, max_length=255)),
                (
                    "linkedin_organization_id",
                    models.CharField(blank=True, max_length=255),
                ),
                (
                    "linkedin_organization_access_token",
                    models.CharField(blank=True, max_length=255),
                ),
                (
                    "linkedin_organization_refresh_token",
                    models.CharField(blank=True, max_length=255),
                ),
                ("twitter_username", models.CharField(blank=True, max_length=255)),
                ("twitter_client_id", models.CharField(blank=True, max_length=255)),
                ("twitter_client_secret", models.CharField(blank=True, max_length=255)),
                ("twitter_api_key", models.CharField(blank=True, max_length=255)),
                (
                    "twitter_api_key_secret",
                    models.CharField(blank=True, max_length=255),
                ),
                ("twitter_access_token", models.CharField(blank=True, max_length=255)),
                (
                    "twitter_access_token_secret",
                    models.CharField(blank=True, max_length=255),
                ),
                ("twitter_bearer_token", models.CharField(blank=True, max_length=255)),
                ("facebook_page_id", models.CharField(blank=True, max_length=255)),
                (
                    "facebook_page_access_token",
                    models.CharField(blank=True, max_length=255),
                ),
                ("facebook_app_id", models.CharField(blank=True, max_length=255)),
                (
                    "facebook_app_secret_key",
                    models.CharField(blank=True, max_length=255),
                ),
                ("instagram_page_id", models.CharField(blank=True, max_length=255)),
                (
                    "instagram_access_token",
                    models.CharField(blank=True, max_length=255),
                ),
                ("deepl_auth_key", models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddConstraint(
            model_name="setting",
            constraint=models.CheckConstraint(
                check=models.Q(("singleton", True)), name="single_setting_model"
            ),
        ),
    ]
