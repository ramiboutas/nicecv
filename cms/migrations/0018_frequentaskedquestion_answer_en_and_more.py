# Generated by Django 4.2.2 on 2023-08-02 20:39
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0017_frequentaskedquestion"),
    ]

    operations = [
        migrations.AddField(
            model_name="frequentaskedquestion",
            name="answer_en",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="frequentaskedquestion",
            name="answer_es",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="frequentaskedquestion",
            name="question_en",
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="frequentaskedquestion",
            name="question_es",
            field=models.CharField(max_length=128, null=True),
        ),
    ]
