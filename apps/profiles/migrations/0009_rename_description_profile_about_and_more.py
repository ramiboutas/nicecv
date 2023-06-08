# Generated by Django 4.1.7 on 2023-06-05 21:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0008_profile_birth_active_profile_email_active_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="description",
            new_name="about",
        ),
        migrations.RenameField(
            model_name="profile",
            old_name="description_label",
            new_name="about_label",
        ),
        migrations.RenameField(
            model_name="profile",
            old_name="description_rows",
            new_name="about_rows",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="description_active",
        ),
        migrations.AddField(
            model_name="profile",
            name="about_active",
            field=models.BooleanField(default=True, verbose_name="About me"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="achievement_active",
            field=models.BooleanField(default=False, verbose_name="Achievements"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="birth_active",
            field=models.BooleanField(default=True, verbose_name="Birth date"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="education_active",
            field=models.BooleanField(default=True, verbose_name="Education"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="email_active",
            field=models.BooleanField(default=True, verbose_name="Email address"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="experience_active",
            field=models.BooleanField(default=True, verbose_name="Work experience"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="jobtitle_active",
            field=models.BooleanField(default=True, verbose_name="Job title"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="language_active",
            field=models.BooleanField(default=False, verbose_name="Languages"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="location_active",
            field=models.BooleanField(default=True, verbose_name="Location"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone_active",
            field=models.BooleanField(default=True, verbose_name="Phone number"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="photo_active",
            field=models.BooleanField(default=True, verbose_name="Photo"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="project_active",
            field=models.BooleanField(default=False, verbose_name="Projects"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="publication_active",
            field=models.BooleanField(default=False, verbose_name="Publications"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="skill_active",
            field=models.BooleanField(default=True, verbose_name="Skills"),
        ),
    ]