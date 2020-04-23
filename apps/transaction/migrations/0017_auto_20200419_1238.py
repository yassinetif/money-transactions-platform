# Generated by Django 3.0.4 on 2020-04-19 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0016_auto_20200418_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='parent',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(default='01100575', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='number',
            field=models.CharField(default='4044104524', max_length=11, unique=True),
        ),
    ]