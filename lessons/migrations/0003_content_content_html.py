# Generated by Django 4.0.2 on 2022-03-03 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_alter_progress_lesson02_alter_progress_lesson03_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='content_html',
            field=models.CharField(blank=True, default='', max_length=10000, null=True),
        ),
    ]
