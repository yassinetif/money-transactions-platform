# Generated by Django 3.0.4 on 2020-03-19 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('entity', '0003_auto_20200319_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default='9917694939', max_length=11, unique=True)),
                ('code', models.CharField(default='12129115', max_length=11, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('source_object_id', models.PositiveIntegerField()),
                ('destination_object_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='entity.Agent')),
                ('destination_content_type', models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'entity'), ('model', 'entity')), models.Q(('app_label', 'kyc'), ('model', 'customer')), _connector='OR'), on_delete=django.db.models.deletion.DO_NOTHING, related_name='destination_content_type', to='contenttypes.ContentType')),
                ('source_content_type', models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'entity'), ('model', 'entity')), models.Q(('app_label', 'kyc'), ('model', 'customer')), _connector='OR'), on_delete=django.db.models.deletion.DO_NOTHING, related_name='source_content_type', to='contenttypes.ContentType')),
            ],
        ),
    ]
