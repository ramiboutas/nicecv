# Generated by Django 4.1.7 on 2023-06-18 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cvtex",
            name="interpreter_options",
            field=models.CharField(
                default="",
                editable=False,
                help_text="Read from metadata",
                max_length=64,
            ),
        ),
    ]
