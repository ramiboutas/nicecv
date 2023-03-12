# Generated by Django 4.1.7 on 2023-03-11 12:56
import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tex", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="coverlettertemplate",
            options={"base_manager_name": "prefetch_manager"},
        ),
        migrations.AlterModelOptions(
            name="resumetemplate",
            options={"base_manager_name": "prefetch_manager"},
        ),
        migrations.AlterModelManagers(
            name="coverlettertemplate",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="resumetemplate",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
