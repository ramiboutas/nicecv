# Generated by Django 4.2.2 on 2023-08-05 09:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_delete_planfaq"),
    ]

    operations = [
        migrations.AddField(
            model_name="premiumplan",
            name="description_de",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="premiumplan",
            name="name_de",
            field=models.CharField(max_length=32, null=True),
        ),
    ]