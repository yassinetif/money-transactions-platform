# Generated by Django 3.0.4 on 2020-04-13 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0006_auto_20200413_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(default='32984506', max_length=11),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='number',
            field=models.CharField(default='2304425837', max_length=11),
        ),
    ]
