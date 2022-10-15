# Generated by Django 4.0.3 on 2022-03-17 21:17

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoverLetterTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('file', models.FileField(upload_to='texfiles/coverletters')),
                ('cls', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/rami/texmf/tex/latex/local'), upload_to='')),
                ('interpreter', models.CharField(default='lualatex', max_length=20)),
                ('image', models.ImageField(upload_to='texfiles/coverletters/screenshots')),
                ('is_active', models.BooleanField(default=True)),
                ('credits', models.CharField(blank=True, max_length=128, null=True)),
                ('credits_url', models.URLField(blank=True, null=True)),
                ('downloads', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ResumeTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('template_name', models.CharField(default='test.tex', max_length=20)),
                ('only_one_page_allowed', models.BooleanField(default=False)),
                ('interpreter', models.CharField(default='lualatex', max_length=20)),
                ('image', models.ImageField(upload_to='tex_screenshots')),
                ('is_active', models.BooleanField(default=True)),
                ('credits', models.CharField(blank=True, max_length=50, null=True)),
                ('credits_url', models.URLField(blank=True, max_length=100, null=True)),
                ('downloads', models.IntegerField(default=0)),
            ],
        ),
    ]
