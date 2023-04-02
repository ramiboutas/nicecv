# Generated by Django 4.1.7 on 2023-04-02 12:44

import auto_prefetch
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0003_alter_skill_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="skill",
            options={"base_manager_name": "prefetch_manager", "verbose_name": "Skills"},
        ),
        migrations.RemoveField(
            model_name="skill",
            name="level",
        ),
        migrations.RemoveField(
            model_name="skill",
            name="name",
        ),
        migrations.AlterField(
            model_name="skill",
            name="profile",
            field=auto_prefetch.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="profiles.profile"
            ),
        ),
        migrations.CreateModel(
            name="SkillItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("level", models.IntegerField(default=50)),
                (
                    "profile",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
                (
                    "skill",
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="profiles.skill",
                    ),
                ),
            ],
            options={
                "ordering": ("-level",),
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
