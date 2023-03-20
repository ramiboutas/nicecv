# Generated by Django 4.1.7 on 2023-03-18 11:07
import auto_prefetch
import django.db.models.deletion
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_alter_userpremiumplan_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userpremiumplan",
            name="user",
            field=auto_prefetch.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user_premium_plans",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
