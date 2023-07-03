# Generated by Django 4.2.2 on 2023-06-30 20:55
import django.db.models.manager
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_remove_language_name_de_remove_language_name_es_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeeplLanguage",
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
                ("name", models.CharField(max_length=32)),
                ("is_source", models.BooleanField(default=False)),
                ("is_target", models.BooleanField(default=False)),
                ("supports_formality", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name="profile",
            name="lang",
        ),
        migrations.AddField(
            model_name="profile",
            name="language_code",
            field=models.CharField(
                default="en", max_length=64, null=True, verbose_name="Language code"
            ),
        ),
        migrations.DeleteModel(
            name="Language",
        ),
    ]
