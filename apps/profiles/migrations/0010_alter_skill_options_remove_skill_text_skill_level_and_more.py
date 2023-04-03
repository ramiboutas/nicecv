# Generated by Django 4.1.7 on 2023-04-02 21:20

import auto_prefetch
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0009_rename_set_skillitem_skill_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="skill",
            options={
                "base_manager_name": "prefetch_manager",
                "ordering": ("-level",),
                "verbose_name": "Skills",
            },
        ),
        migrations.RemoveField(
            model_name="skill",
            name="text",
        ),
        migrations.AddField(
            model_name="skill",
            name="level",
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name="skill",
            name="name",
            field=models.CharField(default="hello", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="skill",
            name="profile",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="profiles.profile"
            ),
        ),
        migrations.DeleteModel(
            name="SkillItem",
        ),
    ]