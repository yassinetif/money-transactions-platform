# Generated by Django 3.0.4 on 2020-04-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0008_auto_20200405_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='account_number',
            field=models.CharField(default='214969945', max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='code',
            field=models.CharField(default='412465', max_length=10, unique=True),
        ),
    ]
