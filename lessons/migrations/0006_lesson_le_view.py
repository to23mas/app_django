# Generated by Django 4.0.2 on 2022-03-03 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0005_content_content_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='le_view',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
