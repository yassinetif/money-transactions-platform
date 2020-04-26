# Generated by Django 3.0.4 on 2020-04-17 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0016_auto_20200413_1608'),
        ('transaction', '0008_auto_20200415_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='destination_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='transaction_destination_country', to='shared.Country'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='source_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='transaction_source_country', to='shared.Country'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(default='19166628', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='number',
            field=models.CharField(default='0119560222', max_length=11, unique=True),
        ),
    ]
