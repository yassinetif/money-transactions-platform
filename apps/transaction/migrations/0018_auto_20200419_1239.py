# Generated by Django 3.0.4 on 2020-04-19 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0017_auto_20200419_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='parent_transaction_number',
            field=models.CharField(blank=True, default='1598487785', max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(default='22180490', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='number',
            field=models.CharField(default='0237579023', max_length=11, unique=True),
        ),
    ]