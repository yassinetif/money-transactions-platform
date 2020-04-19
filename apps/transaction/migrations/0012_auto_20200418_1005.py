# Generated by Django 3.0.4 on 2020-04-18 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0011_auto_20200418_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='code',
            field=models.CharField(default='20095800', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='number',
            field=models.CharField(default='1132835514', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.Transaction'),
        ),
    ]
