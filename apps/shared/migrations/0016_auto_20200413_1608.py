# Generated by Django 3.0.4 on 2020-04-13 16:08

from django.db import migrations, models
import shared.models.price


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0015_auto_20200413_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='grille',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sharing',
            name='calculation_expression',
            field=models.CharField(help_text='FRAIS/2->PROVIDER:0.2:CREDIT;BANQUE:0.4:CREDIT',
                                   max_length=200, validators=[shared.models.price.validate_calculation_expression]),
        ),
    ]
