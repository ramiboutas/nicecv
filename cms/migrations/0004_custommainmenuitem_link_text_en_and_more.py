# Generated by Django 4.2.2 on 2023-07-10 18:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0003_custommainmenu_custommainmenuitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="custommainmenuitem",
            name="link_text_en",
            field=models.CharField(
                blank=True,
                help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.",
                max_length=255,
                null=True,
                verbose_name="link text",
            ),
        ),
        migrations.AddField(
            model_name="custommainmenuitem",
            name="link_text_es",
            field=models.CharField(
                blank=True,
                help_text="Provide the text to use for a custom URL, or set on an internal page link to use instead of the page's title.",
                max_length=255,
                null=True,
                verbose_name="link text",
            ),
        ),
    ]