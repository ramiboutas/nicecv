# Generated by Django 4.1.7 on 2023-04-02 15:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0006_remove_skillitem_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="skill",
            name="text",
            field=models.CharField(
                blank=True, max_length=32, null=True, verbose_name="Website"
            ),
        ),
    ]
