# Generated by Django 4.0.2 on 2022-04-03 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_alter_content_content_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_text',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
