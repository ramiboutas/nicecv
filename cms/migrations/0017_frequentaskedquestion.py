# Generated by Django 4.2.2 on 2023-08-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0016_alter_homepage_body"),
    ]

    operations = [
        migrations.CreateModel(
            name="FrequentAskedQuestion",
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
                ("question", models.CharField(max_length=128)),
                ("answer", models.TextField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("pricing", "Related to Pricing"),
                            ("featured", "Featured"),
                        ],
                        max_length=16,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
            ],
        ),
    ]
