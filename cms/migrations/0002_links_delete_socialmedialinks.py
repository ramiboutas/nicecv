# Generated by Django 4.2.5 on 2024-01-07 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Links",
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
                (
                    "facebook",
                    models.URLField(blank=True, help_text="Facebook URL", null=True),
                ),
                (
                    "twitter",
                    models.URLField(blank=True, help_text="Twitter URL", null=True),
                ),
                (
                    "youtube",
                    models.URLField(
                        blank=True, help_text="YouTube Channel URL", null=True
                    ),
                ),
                (
                    "linkedin",
                    models.URLField(blank=True, help_text="Linkedin URL", null=True),
                ),
                (
                    "github",
                    models.URLField(blank=True, help_text="GitHub URL", null=True),
                ),
                (
                    "instagram",
                    models.URLField(blank=True, help_text="Instagram URL", null=True),
                ),
                (
                    "whatsapp",
                    models.URLField(blank=True, help_text="Whatapp URL", null=True),
                ),
                (
                    "telegram",
                    models.URLField(blank=True, help_text="Telegram URL", null=True),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, help_text="Email Address", max_length=254, null=True
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="SocialMediaLinks",
        ),
    ]
