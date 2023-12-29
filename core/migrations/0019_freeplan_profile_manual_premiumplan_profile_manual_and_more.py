# Generated by Django 4.2.5 on 2023-12-29 12:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0018_alter_achievement_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="freeplan",
            name="profile_manual",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="premiumplan",
            name="profile_manual",
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name="premiumplan",
            constraint=models.UniqueConstraint(
                condition=models.Q(("profile_manual", True)),
                fields=("profile_manual",),
                name="unique_plan_with_manual_profile",
            ),
        ),
    ]
