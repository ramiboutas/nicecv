# Generated by Django 4.1.7 on 2023-03-24 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0002_alter_website_active_location"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SkillSet",
            new_name="Skill",
        ),
        migrations.AlterModelOptions(
            name="birth",
            options={
                "base_manager_name": "prefetch_manager",
                "verbose_name": "Date of birth",
            },
        ),
        migrations.AlterModelOptions(
            name="email",
            options={"base_manager_name": "prefetch_manager", "verbose_name": "Email"},
        ),
        migrations.AlterModelOptions(
            name="fullname",
            options={
                "base_manager_name": "prefetch_manager",
                "verbose_name": "Full name",
            },
        ),
        migrations.AlterModelOptions(
            name="jobtitle",
            options={
                "base_manager_name": "prefetch_manager",
                "verbose_name": "Job title",
            },
        ),
        migrations.AlterModelOptions(
            name="location",
            options={
                "base_manager_name": "prefetch_manager",
                "verbose_name": "Location",
            },
        ),
        migrations.AlterModelOptions(
            name="phone",
            options={
                "base_manager_name": "prefetch_manager",
                "verbose_name": "Phone number",
            },
        ),
        migrations.AlterModelOptions(
            name="website",
            options={
                "base_manager_name": "prefetch_manager",
                "verbose_name": "Website",
            },
        ),
        migrations.AlterField(
            model_name="birth",
            name="text",
            field=models.CharField(
                blank=True, max_length=16, null=True, verbose_name="Date of birth"
            ),
        ),
        migrations.AlterField(
            model_name="email",
            name="text",
            field=models.CharField(
                blank=True, max_length=32, null=True, verbose_name="Email"
            ),
        ),
        migrations.AlterField(
            model_name="fullname",
            name="text",
            field=models.CharField(
                blank=True, max_length=32, null=True, verbose_name="Full name"
            ),
        ),
        migrations.AlterField(
            model_name="jobtitle",
            name="text",
            field=models.CharField(
                blank=True, max_length=16, null=True, verbose_name="Job title"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="text",
            field=models.CharField(
                blank=True, max_length=16, null=True, verbose_name="Location"
            ),
        ),
        migrations.AlterField(
            model_name="phone",
            name="text",
            field=models.CharField(
                blank=True, max_length=16, null=True, verbose_name="Phone number"
            ),
        ),
        migrations.AlterField(
            model_name="website",
            name="text",
            field=models.CharField(
                blank=True, max_length=16, null=True, verbose_name="Website"
            ),
        ),
    ]
