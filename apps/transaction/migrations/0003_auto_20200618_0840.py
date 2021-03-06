# Generated by Django 3.0.4 on 2020-06-18 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20200521_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='other_informations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(default='03211315', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='number',
            field=models.CharField(default='4452297709', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='parent_transaction_number',
            field=models.CharField(blank=True, default='4861043123', max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('CASH_TO_CASH', 'CASH_TO_CASH'), ('CASH_TO_WALLET', 'CASH_TO_WALLET'), ('WALLET_TO_CASH', 'WALLET_TO_CASH'), ('WALLET_TO_WALLET', 'WALLET_TO_WALLET'), ('RETRAIT_CASH', 'RETRAIT_CASH'), ('ACTIVATION_CARTE', 'ACTIVATION_CARTE'), ('CREATION_WALLET', 'CREATION_WALLET'), ('CREDIT_COMPTE_ENTITE', 'CREDIT_COMPTE_ENTITE'), ('DEBIT_COMPTE_ENTITE', 'DEBIT_COMPTE_ENTITE'), ('CASH_TO_BANK_ACCOUNT', 'CASH_TO_BANK_ACCOUNT'), ('WALLET_TO_BANK_ACCOUNT', 'WALLET_TO_BANK_ACCOUNT')], default='CASH_TO_CASH', max_length=30),
        ),
    ]
