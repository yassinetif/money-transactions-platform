# Generated by Django 3.0.4 on 2020-07-23 11:34

import apps.core.utils.string
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0006_auto_20200723_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=apps.core.utils.string.entity_logo_directory_path),
        ),
        migrations.AlterField(
            model_name='agent',
            name='code',
            field=models.CharField(default='872904', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='account_number',
            field=models.CharField(default='104438156', max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='code',
            field=models.CharField(default='942330', max_length=10, unique=True),
        ),
    ]
