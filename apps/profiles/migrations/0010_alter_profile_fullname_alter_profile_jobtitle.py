# Generated by Django 4.1.7 on 2023-03-19 21:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0009_alter_profile_birth_alter_profile_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="fullname",
            field=models.CharField(
                blank=True, max_length=32, null=True, verbose_name="Full name"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="jobtitle",
            field=models.CharField(
                blank=True, max_length=32, null=True, verbose_name="Job title"
            ),
        ),
    ]
