# Generated by Django 4.2.2 on 2023-07-13 16:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0005_customflatmenuitem_link_text_en_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="custommainmenuitem",
            name="add_to_profile_dropdown",
            field=models.BooleanField(default=False),
        ),
    ]