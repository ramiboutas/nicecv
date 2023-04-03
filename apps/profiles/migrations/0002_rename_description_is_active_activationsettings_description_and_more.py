# Generated by Django 4.1.7 on 2023-03-28 05:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="activationsettings",
            old_name="description_is_active",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="activationsettings",
            old_name="skill_set_is_active",
            new_name="skill_set",
        ),
        migrations.AddField(
            model_name="activationsettings",
            name="website",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="labelsettings",
            name="website",
            field=models.CharField(default="Website", max_length=32),
        ),
    ]