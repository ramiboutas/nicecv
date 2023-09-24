# Generated by Django 4.2.3 on 2023-08-22 09:53

import core.models.profiles
import django.core.files.storage
from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_alter_profile_cropped_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="cropped_photo",
            field=models.ImageField(
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    base_url="localhost:8000/media/",
                    location=pathlib.PurePosixPath(
                        "/home/rami/Documents/GitHub/nicecv/media"
                    ),
                ),
                upload_to=core.models.profiles.get_photo_upload_path,
            ),
        ),
    ]
