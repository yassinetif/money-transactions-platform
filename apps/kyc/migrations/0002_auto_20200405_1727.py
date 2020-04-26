# Generated by Django 3.0.4 on 2020-04-05 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0006_auto_20200405_1645'),
        ('kyc', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Client'},
        ),
        migrations.AddField(
            model_name='customer',
            name='identification_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='identification_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='issuer_country',
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared.Country'),
        ),
    ]
