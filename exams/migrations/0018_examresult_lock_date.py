# Generated by Django 4.0.2 on 2022-03-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0017_alter_examresult_lock'),
    ]

    operations = [
        migrations.AddField(
            model_name='examresult',
            name='lock_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
