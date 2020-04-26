# Generated by Django 3.0.4 on 2020-03-19 21:10

from django.db import migrations, models
import entity.models.entity


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0003_auto_20200319_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='catetory',
            field=models.CharField(choices=[(entity.models.entity.EntityType['PROVIDER'], 'PROVIDER'), (
                entity.models.entity.EntityType['DISTRIBUTEUR'], 'DISTRIBUTEUR'), (entity.models.entity.EntityType['BANQUE'], 'BANQUE')], max_length=5),
        ),
        migrations.AlterField(
            model_name='entity',
            name='code',
            field=models.CharField(default='881349', max_length=10, unique=True),
        ),
    ]
