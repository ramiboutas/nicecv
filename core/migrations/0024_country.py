# Generated by Django 4.2.5 on 2024-01-04 19:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0023_user_asked_to_verify_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
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
                ("code", models.CharField(max_length=8)),
                ("name", models.CharField(max_length=64)),
                ("gdp", models.PositiveIntegerField(default=50000)),
                ("currency", models.CharField(max_length=8)),
                ("wikipedia_url", models.URLField(max_length=128)),
            ],
        ),
    ]
