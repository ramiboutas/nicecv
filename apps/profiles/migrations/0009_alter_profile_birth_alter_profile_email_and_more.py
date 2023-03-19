# Generated by Django 4.1.7 on 2023-03-19 18:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0008_remove_profile_birth_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="birth",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Date of birth"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="email",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Email address"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="fullname",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Full name"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="jobtitle",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Job title"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="location",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Location"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Phone number"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="website",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Website"
            ),
        ),
    ]
