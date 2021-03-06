# Generated by Django 3.0.4 on 2020-05-21 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='127642', max_length=10, unique=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('authentication_type', models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('OTP', 'OTP')], default='DEFAULT', max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agents',
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='198752', max_length=10, unique=True)),
                ('account_number', models.CharField(default='864741944', max_length=9, unique=True)),
                ('category', models.CharField(choices=[('PROVIDER', 'PROVIDER'), ('DISTRIBUTEUR', 'DISTRIBUTEUR'), ('BANQUE', 'BANQUE'), ('BUSINESS_PARTNER', 'BUSINESS_PARTNER')], default='PROVIDER', max_length=30)),
                ('brand_name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
            },
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
                'verbose_name_plural': 'Entities settings',
            },
        ),
    ]
