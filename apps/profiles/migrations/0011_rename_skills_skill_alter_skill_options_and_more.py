# Generated by Django 4.1.7 on 2023-03-25 11:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0010_alter_skills_options"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Skills",
            new_name="Skill",
        ),
        migrations.AlterModelOptions(
            name="skill",
            options={
                "base_manager_name": "prefetch_manager",
                "default_related_name": "skill_set",
            },
        ),
        migrations.RenameField(
            model_name="active",
            old_name="skill",
            new_name="skill_set",
        ),
        migrations.RenameField(
            model_name="label",
            old_name="skills",
            new_name="skill_set",
        ),
    ]
