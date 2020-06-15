# Generated by Django 3.0.4 on 2020-06-15 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0004_auto_20200527_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotifEnvoi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('libelle', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Motif Envoi',
            },
        ),
        migrations.CreateModel(
            name='SourceRevenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('libelle', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Source de revenus',
            },
        ),
    ]