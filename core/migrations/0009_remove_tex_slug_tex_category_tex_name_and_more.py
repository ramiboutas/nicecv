# Generated by Django 4.2.3 on 2023-08-26 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_alter_profile_cropped_photo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tex",
            name="slug",
        ),
        migrations.AddField(
            model_name="tex",
            name="category",
            field=models.CharField(default="cvs", editable=False, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tex",
            name="name",
            field=models.CharField(default="DummyName", editable=False, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="tex",
            name="template_name",
            field=models.CharField(editable=False, max_length=64, unique=True),
        ),
    ]