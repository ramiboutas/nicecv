# Generated by Django 4.1.7 on 2023-03-11 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0003_planfaq_plan_name_plan_name_de_plan_name_en_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='name_fr',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='name_it',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='name_pt',
        ),
        migrations.RemoveField(
            model_name='planfaq',
            name='answer_fr',
        ),
        migrations.RemoveField(
            model_name='planfaq',
            name='answer_it',
        ),
        migrations.RemoveField(
            model_name='planfaq',
            name='answer_pt',
        ),
        migrations.RemoveField(
            model_name='planfaq',
            name='question_fr',
        ),
        migrations.RemoveField(
            model_name='planfaq',
            name='question_it',
        ),
        migrations.RemoveField(
            model_name='planfaq',
            name='question_pt',
        ),
    ]
