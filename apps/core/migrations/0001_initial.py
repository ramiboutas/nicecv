# Generated by Django 4.1.7 on 2023-03-28 05:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Settings",
            fields=[
                (
                    "the_singleton",
                    models.BooleanField(
                        default=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "setting_a",
                    models.CharField(blank=True, default="Setting A", max_length=255),
                ),
                ("setting_b", models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.AddConstraint(
            model_name="settings",
            constraint=models.CheckConstraint(
                check=models.Q(("the_singleton", True)), name="single_setting_model"
            ),
        ),
    ]