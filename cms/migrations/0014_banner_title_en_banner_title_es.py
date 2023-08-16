# Generated by Django 4.2.2 on 2023-08-01 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0013_banner_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="banner",
            name="title_en",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="banner",
            name="title_es",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]