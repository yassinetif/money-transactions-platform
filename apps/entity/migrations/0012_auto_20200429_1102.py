# Generated by Django 3.0.4 on 2020-04-29 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0011_auto_20200429_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='code',
            field=models.CharField(default='690665', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='account_number',
            field=models.CharField(default='355778809', max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='code',
            field=models.CharField(default='044023', max_length=10, unique=True),
        ),
        migrations.CreateModel(
            name='EntitySettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_entity_balance', models.BooleanField(default=True, help_text='Check Entity balance before processing operation')),
                ('overdraft_amount', models.DecimalField(decimal_places=2, default=0, help_text='Overdraft amount', max_digits=7)),
                ('entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='entity.Entity')),
            ],
            options={
                'verbose_name': 'Entity setting',
            },
        ),
    ]
