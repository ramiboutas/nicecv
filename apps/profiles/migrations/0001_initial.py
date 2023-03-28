# Generated by Django 4.1.7 on 2023-03-28 05:32

import apps.profiles.models
import auto_prefetch
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sessions", "0001_initial"),
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("temporal", "Temporal"),
                            ("user_profile", "User profile"),
                            ("template", "Template"),
                        ],
                        default="user_profile",
                        max_length=16,
                    ),
                ),
                ("public", models.BooleanField(default=False)),
                (
                    "slug",
                    models.SlugField(blank=True, max_length=16, null=True, unique=True),
                ),
                (
                    "session",
                    auto_prefetch.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_set",
                        to="sessions.session",
                    ),
                ),
                (
                    "user",
                    auto_prefetch.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="profile_set",
                        to=settings.AUTH_USER_MODEL,
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
        migrations.CreateModel(
            name="Website",
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
                (
                    "text",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="Website"
                    ),
                ),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Website",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
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
                    auto_prefetch.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "ordering": ("-level",),
                "abstract": False,
                "default_related_name": "skill_set",
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="Photo",
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
                (
                    "full",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.profiles.models.get_uploading_photo_path,
                    ),
                ),
                (
                    "cropped",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.profiles.models.get_uploading_photo_path,
                    ),
                ),
                ("crop_x", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("crop_y", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("crop_width", models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    "crop_height",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
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
        migrations.CreateModel(
            name="Phone",
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
                (
                    "text",
                    models.CharField(
                        blank=True,
                        max_length=16,
                        null=True,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Phone number",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="Location",
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
                (
                    "text",
                    models.CharField(
                        blank=True, max_length=16, null=True, verbose_name="Location"
                    ),
                ),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Location",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="LabelSettings",
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
                ("skill_set", models.CharField(default="Skills", max_length=32)),
                ("description", models.CharField(default="About me", max_length=32)),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
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
        migrations.CreateModel(
            name="Jobtitle",
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
                (
                    "text",
                    models.CharField(
                        blank=True, max_length=16, null=True, verbose_name="Job title"
                    ),
                ),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Job title",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="Fullname",
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
                (
                    "text",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="Full name"
                    ),
                ),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Full name",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="Email",
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
                (
                    "text",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="Email"
                    ),
                ),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Email",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
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
        migrations.CreateModel(
            name="Birth",
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
                (
                    "text",
                    models.CharField(
                        blank=True,
                        max_length=16,
                        null=True,
                        verbose_name="Date of birth",
                    ),
                ),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Date of birth",
                "abstract": False,
                "base_manager_name": "prefetch_manager",
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name="ActivationSettings",
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
                ("skill_set_is_active", models.BooleanField(default=False)),
                ("description_is_active", models.BooleanField(default=True)),
                (
                    "profile",
                    auto_prefetch.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
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
