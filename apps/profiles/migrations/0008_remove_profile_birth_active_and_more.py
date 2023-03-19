# Generated by Django 4.1.7 on 2023-03-19 17:00

import auto_prefetch
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0007_alter_skillitem_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="birth_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="certification_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="certification_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="course_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="course_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="description",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="description_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="description_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="education_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="education_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="email_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="experience_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="experience_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="facebook_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="github_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="gitlab_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="honor_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="honor_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="instagram_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="jobtitle_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="language_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="language_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="linkedin_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="location_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="medium_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="orcid_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="organization_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="organization_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="patent_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="patent_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="phone_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="project_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="project_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="publication_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="publication_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="skill_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="skill_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="skype_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="stackoverflow_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="twitter_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="volunteering_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="volunteering_label",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="website_active",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="youtube_active",
        ),
        migrations.AddField(
            model_name="skillset",
            name="label",
            field=models.CharField(default="Skills", max_length=100),
        ),
        migrations.CreateModel(
            name="Description",
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
                ("active", models.BooleanField(default=True)),
                ("label", models.CharField(default="About me", max_length=100)),
                ("text", models.TextField()),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
    ]
