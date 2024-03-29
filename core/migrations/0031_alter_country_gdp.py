# Generated by Django 4.2.5 on 2024-01-06 01:27

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0030_alter_profile_cropped_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="gdp",
            field=models.DecimalField(
                decimal_places=3, default=Decimal("50000"), max_digits=12
            ),
        ),
    ]
