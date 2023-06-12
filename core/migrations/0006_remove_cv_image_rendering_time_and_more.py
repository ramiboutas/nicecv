# Generated by Django 4.1.7 on 2023-06-12 19:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_cv_image_rendering_time_cv_pdf_rendering_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cv",
            name="image_rendering_time",
        ),
        migrations.RemoveField(
            model_name="cv",
            name="pdf_rendering_time",
        ),
        migrations.RemoveField(
            model_name="cv",
            name="rendering_time",
        ),
        migrations.AddField(
            model_name="cv",
            name="image_time",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="cv",
            name="pdf_time",
            field=models.FloatField(default=0),
        ),
    ]
