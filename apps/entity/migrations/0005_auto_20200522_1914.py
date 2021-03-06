# Generated by Django 3.0.4 on 2020-05-22 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0004_auto_20200521_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='code',
            field=models.CharField(default='416213', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='account_number',
            field=models.CharField(default='006300897', max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='code',
            field=models.CharField(default='034807', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='entitysettings',
            name='overdraft_amount',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Overdraft amount', max_digits=15),
        ),
    ]
