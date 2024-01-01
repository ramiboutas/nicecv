# Generated by Django 4.2.5 on 2023-12-24 20:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_alter_profile_cropped_photo"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Secrets",
        ),
        migrations.AlterModelOptions(
            name="cv",
            options={
                "base_manager_name": "prefetch_manager",
                "ordering": ["-created_on"],
            },
        ),
        migrations.RenameField(
            model_name="cv",
            old_name="created",
            new_name="created_on",
        ),
    ]