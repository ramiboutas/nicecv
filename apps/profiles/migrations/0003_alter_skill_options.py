# Generated by Django 4.1.7 on 2023-04-02 09:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "profiles",
            "0002_rename_description_is_active_activationsettings_description_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="skill",
            options={
                "base_manager_name": "prefetch_manager",
                "default_related_name": "skill",
                "ordering": ("-level",),
            },
        ),
    ]
