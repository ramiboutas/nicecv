# Generated by Django 4.2.2 on 2023-08-01 19:11
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("cms", "0009_alter_banner_page_alter_banner_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="banner",
            name="page_en",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="wagtailcore.page",
            ),
        ),
        migrations.AddField(
            model_name="banner",
            name="page_es",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="wagtailcore.page",
            ),
        ),
        migrations.AddField(
            model_name="banner",
            name="text_en",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="banner",
            name="text_es",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name="FixedBanner",
        ),
    ]
