# Generated by Django 4.2.2 on 2023-07-31 20:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0004_rename_blogpost_blogpostpage_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpostpage",
            name="description",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]