# Generated by Django 4.2.5 on 2023-12-28 11:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0017_alter_education_institution_alter_experience_company_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="achievement",
            name="title",
            field=models.CharField(max_length=64, verbose_name="🏆 Goal achieved"),
        ),
    ]
