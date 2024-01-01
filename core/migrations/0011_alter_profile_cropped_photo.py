# Generated by Django 4.2.5 on 2023-12-23 16:45

import core.models.profiles
import django.core.files.storage
from django.db import migrations, models
import pathlib


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_alter_premiumplan_price_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="cropped_photo",
            field=models.ImageField(
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    base_url="/media/",
                    location=pathlib.PurePosixPath("/home/rami/dev/nicecv/media"),
                ),
                upload_to=core.models.profiles.get_photo_upload_path,
            ),
        ),
    ]