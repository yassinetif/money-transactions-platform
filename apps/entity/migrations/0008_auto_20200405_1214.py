# Generated by Django 3.0.4 on 2020-04-05 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0007_auto_20200321_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='account_number',
            field=models.CharField(default='598237054', max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='category',
            field=models.CharField(choices=[('PROVIDER', 'PROVIDER'), (
                'DISTRIBUTEUR', 'DISTRIBUTEUR'), ('BANQUE', 'BANQUE')], default='PROVIDER', max_length=30),
        ),
        migrations.AlterField(
            model_name='entity',
            name='code',
            field=models.CharField(default='203430', max_length=10, unique=True),
        ),
    ]
