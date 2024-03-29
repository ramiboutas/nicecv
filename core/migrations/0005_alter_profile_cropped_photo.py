# Generated by Django 4.2.3 on 2023-08-22 09:37

import core.models.profiles
import django.core.files.storage
from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_remove_user_notify_when_plan_expires"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="cropped_photo",
            field=models.ImageField(
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location=pathlib.PurePosixPath(
                        "/home/rami/Documents/GitHub/nicecv/media"
                    )
                ),
                upload_to=core.models.profiles.get_photo_upload_path,
            ),
        ),
    ]
