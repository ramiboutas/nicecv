# Generated by Django 4.1.7 on 2023-06-04 12:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0038_alter_fullname_options_alter_fullname_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="first_name",
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="last_name",
            field=models.CharField(max_length=16, null=True),
        ),
    ]
