# Generated by Django 4.1.7 on 2023-03-11 12:56
import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("plans", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"base_manager_name": "prefetch_manager"},
        ),
        migrations.AlterModelOptions(
            name="plan",
            options={
                "base_manager_name": "prefetch_manager",
                "ordering": ("months", "price"),
            },
        ),
        migrations.AlterModelManagers(
            name="order",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="plan",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("prefetch_manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveConstraint(
            model_name="plan",
            name="unique_default_field",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="default",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="saving",
        ),
        migrations.RemoveField(
            model_name="plan",
            name="stripe_product_id",
        ),
        migrations.AddField(
            model_name="plan",
            name="max_profiles",
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name="order",
            name="plan",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="plans.plan"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=auto_prefetch.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]