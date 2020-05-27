# Generated by Django 3.0.4 on 2020-05-22 17:11

import apps.core.utils.string
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grille',
            name='name',
        ),
        migrations.AlterField(
            model_name='sharing',
            name='calculation_expression',
            field=models.CharField(help_text='FEE/2=>PROVIDER:0.2:+;BANQUE:0.4:-', max_length=200, validators=[apps.core.utils.string.validate_calculation_expression]),
        ),
    ]