# Generated by Django 4.1.7 on 2023-06-23 05:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tex",
            old_name="credits_url",
            new_name="source_url",
        ),
    ]
