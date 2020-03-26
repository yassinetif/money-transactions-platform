from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from entity.models import Agent
from core.utils import random_code

class Transaction(models.Model):
    number = models.CharField(
        max_length=11, default=random_code(10), unique=True, blank=False, null=False)
    code = models.CharField(
        max_length=11, default=random_code(8), unique=True, blank=False, null=False)

    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    limit = models.Q(app_label='entity', model='entity') \
        | models.Q(app_label='kyc', model='customer')

    source_content_type = models.ForeignKey(
        ContentType, related_name="source_content_type", null=False, blank=False, limit_choices_to=limit, on_delete=models.DO_NOTHING)
    source_object_id = models.PositiveIntegerField()
    source_content_object = GenericForeignKey(
        'source_content_type', 'source_object_id')

    destination_content_type = models.ForeignKey(
        ContentType, related_name="destination_content_type", null=False, blank=False, limit_choices_to=limit, on_delete=models.DO_NOTHING)
    destination_object_id = models.PositiveIntegerField()
    destination_content_object = GenericForeignKey(
        'destination_content_type', 'destination_object_id')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tranaction"
        verbose_name_plural = "Transactions"
