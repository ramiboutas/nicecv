# Generated by Django 4.1.2 on 2023-02-28 20:30
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("texfiles", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("task_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="profiles/cropped_photos/"
                    ),
                ),
                (
                    "photo_full",
                    models.ImageField(
                        blank=True, null=True, upload_to="profiles/full_photos/"
                    ),
                ),
                ("firstname", models.CharField(blank=True, max_length=50, null=True)),
                ("lastname", models.CharField(blank=True, max_length=50, null=True)),
                ("jobtitle", models.CharField(max_length=50)),
                ("location", models.CharField(blank=True, max_length=50, null=True)),
                ("birth", models.CharField(blank=True, max_length=50, null=True)),
                ("phone", models.CharField(blank=True, max_length=50, null=True)),
                ("email", models.CharField(blank=True, max_length=50, null=True)),
                ("website", models.CharField(blank=True, max_length=50, null=True)),
                ("linkedin", models.CharField(blank=True, max_length=50, null=True)),
                ("skype", models.CharField(blank=True, max_length=50, null=True)),
                ("instagram", models.CharField(blank=True, max_length=50, null=True)),
                ("twitter", models.CharField(blank=True, max_length=50, null=True)),
                ("facebook", models.CharField(blank=True, max_length=50, null=True)),
                ("youtube", models.CharField(blank=True, max_length=50, null=True)),
                ("github", models.CharField(blank=True, max_length=50, null=True)),
                ("gitlab", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "stackoverflow",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("medium", models.CharField(blank=True, max_length=50, null=True)),
                ("orcid", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                ("interests", models.CharField(blank=True, max_length=200, null=True)),
                ("jobtitle_active", models.BooleanField(default=True)),
                ("location_active", models.BooleanField(default=True)),
                ("birth_active", models.BooleanField(default=True)),
                ("phone_active", models.BooleanField(default=True)),
                ("email_active", models.BooleanField(default=True)),
                ("description_active", models.BooleanField(default=True)),
                ("website_active", models.BooleanField(default=False)),
                ("linkedin_active", models.BooleanField(default=True)),
                ("skype_active", models.BooleanField(default=True)),
                ("instagram_active", models.BooleanField(default=False)),
                ("twitter_active", models.BooleanField(default=False)),
                ("facebook_active", models.BooleanField(default=False)),
                ("youtube_active", models.BooleanField(default=False)),
                ("github_active", models.BooleanField(default=False)),
                ("gitlab_active", models.BooleanField(default=False)),
                ("stackoverflow_active", models.BooleanField(default=False)),
                ("medium_active", models.BooleanField(default=False)),
                ("orcid_active", models.BooleanField(default=False)),
                ("skill_active", models.BooleanField(default=True)),
                ("language_active", models.BooleanField(default=True)),
                ("education_active", models.BooleanField(default=True)),
                ("experience_active", models.BooleanField(default=True)),
                ("certification_active", models.BooleanField(default=False)),
                ("course_active", models.BooleanField(default=True)),
                ("honor_active", models.BooleanField(default=False)),
                ("organization_active", models.BooleanField(default=False)),
                ("patent_active", models.BooleanField(default=False)),
                ("project_active", models.BooleanField(default=False)),
                ("publication_active", models.BooleanField(default=False)),
                ("volunteering_active", models.BooleanField(default=False)),
                (
                    "description_label",
                    models.CharField(default="About me", max_length=100),
                ),
                ("skill_label", models.CharField(default="Skills", max_length=100)),
                (
                    "language_label",
                    models.CharField(default="Languages", max_length=100),
                ),
                (
                    "education_label",
                    models.CharField(default="Education", max_length=100),
                ),
                (
                    "experience_label",
                    models.CharField(default="Work experience", max_length=100),
                ),
                (
                    "certification_label",
                    models.CharField(default="Certifications", max_length=100),
                ),
                ("course_label", models.CharField(default="Courses", max_length=100)),
                (
                    "honor_label",
                    models.CharField(default="Honors and Awards", max_length=100),
                ),
                (
                    "organization_label",
                    models.CharField(default="Organizations", max_length=100),
                ),
                ("patent_label", models.CharField(default="Patents", max_length=100)),
                ("project_label", models.CharField(default="Projects", max_length=100)),
                (
                    "publication_label",
                    models.CharField(default="Publications", max_length=100),
                ),
                (
                    "volunteering_label",
                    models.CharField(default="Volunteering work", max_length=100),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Volunteering",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("location", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "organization",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "organization_link",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("start_date", models.CharField(blank=True, max_length=100, null=True)),
                ("end_date", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="volunteering_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Skill",
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
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="skill_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("-level",),
            },
        ),
        migrations.CreateModel(
            name="Resume",
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
                ("image", models.ImageField(null=True, upload_to="resumes/images")),
                ("pdf", models.FileField(null=True, upload_to="resumes/pdfs")),
                (
                    "profile",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="resumes",
                        to="profiles.profile",
                    ),
                ),
                (
                    "resume_template",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="texfiles.resumetemplate",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Publication",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "issuing_date",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("authors", models.CharField(blank=True, max_length=200, null=True)),
                ("publisher", models.CharField(blank=True, max_length=100, null=True)),
                ("link", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="publication_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Project",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("role", models.CharField(blank=True, max_length=100, null=True)),
                ("start_date", models.CharField(blank=True, max_length=100, null=True)),
                ("end_date", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "organization",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("link", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Patent",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("number", models.CharField(blank=True, max_length=15, null=True)),
                ("issuer", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "issuing_date",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("inventors", models.CharField(blank=True, max_length=200, null=True)),
                ("link", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patent_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Organization",
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
                ("order", models.SmallIntegerField(default=0)),
                ("role", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "organization",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "organization_link",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("start_date", models.CharField(blank=True, max_length=50, null=True)),
                ("end_date", models.CharField(blank=True, max_length=50, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Language",
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
                ("level", models.IntegerField(default=3)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="language_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("id", "level"),
            },
        ),
        migrations.CreateModel(
            name="Honor",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "issuing_date",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("issuer", models.CharField(blank=True, max_length=100, null=True)),
                ("link", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="honor_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Experience",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("location", models.CharField(blank=True, max_length=100, null=True)),
                ("company", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "company_link",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("start_date", models.CharField(blank=True, max_length=100, null=True)),
                ("end_date", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="experience_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Education",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                ("grade", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "institution",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "institution_link",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("start_date", models.CharField(blank=True, max_length=50, null=True)),
                ("end_date", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "description",
                    models.TextField(blank=True, max_length=300, null=True),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="education_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Course",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "issuing_date",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("issuer", models.CharField(blank=True, max_length=100, null=True)),
                ("hours", models.CharField(blank=True, max_length=100, null=True)),
                ("link", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="Certification",
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
                ("order", models.SmallIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "issuing_date",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("issuer", models.CharField(blank=True, max_length=100, null=True)),
                ("link", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="certification_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]