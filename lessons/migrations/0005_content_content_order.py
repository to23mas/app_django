# Generated by Django 4.0.2 on 2022-03-03 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_alter_content_content_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='content_order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
