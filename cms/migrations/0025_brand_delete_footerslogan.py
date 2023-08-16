# Generated by Django 4.2.2 on 2023-08-10 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("wagtailsvg", "0005_alter_svg_file"),
        ("cms", "0024_alter_blogpostpage_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("footer_text", models.TextField(blank=True, null=True)),
                ("footer_text_en", models.TextField(blank=True, null=True)),
                ("footer_text_es", models.TextField(blank=True, null=True)),
                ("footer_text_de", models.TextField(blank=True, null=True)),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
                (
                    "svg",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailsvg.svg",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="FooterSlogan",
        ),
    ]