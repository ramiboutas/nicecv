# Generated by Django 4.2.2 on 2023-08-01 19:03
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("cms", "0008_alter_fixedbanner_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="banner",
            name="page",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="wagtailcore.page",
            ),
        ),
        migrations.AlterField(
            model_name="banner",
            name="text",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
