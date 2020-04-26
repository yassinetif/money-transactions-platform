# Generated by Django 3.0.4 on 2020-04-17 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0009_auto_20200417_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('CASH_TO_CASH', 'CASH_TO_CASH'), (
                'RETRAIT_CASH', 'RETRAIT_CASH')], default='CASH_TO_CASH', max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(default='39281816', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='number',
            field=models.CharField(default='9131641001', max_length=11, unique=True),
        ),
    ]
