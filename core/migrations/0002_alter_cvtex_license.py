# Generated by Django 4.1.7 on 2023-06-14 19:23
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cvtex",
            name="license",
            field=models.CharField(
                editable=False, help_text="Read from metadata", max_length=32
            ),
        ),
    ]
