# Generated by Django 4.0.2 on 2022-03-22 10:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lessons', '0004_remove_lesson_user_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='complete',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
