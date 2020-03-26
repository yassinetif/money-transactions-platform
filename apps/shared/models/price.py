from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from enum import Enum


class TransactionType(Enum):
    ENVOI_CASH = 'ENVOI_CASH'
    RETRAIT_CASH = 'RETRAIT_CASH'


class FeeType(Enum):
    CONST = 'CONSTANTE'
    PERCENT = 'PERCENTAGE'


class Corridor(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    limit = models.Q(app_label='entity', model='entity') \
        | models.Q(app_label='shared', model='country')

    transaction_type = models.CharField(max_length=5, choices=[
        (tag, tag.value) for tag in TransactionType])

    source_content_type = models.ForeignKey(
        ContentType, related_name="corridor_source_content_type", null=False, blank=False, limit_choices_to=limit, on_delete=models.DO_NOTHING)
    source_object_id = models.PositiveIntegerField()
    source_content_object = GenericForeignKey(
        'source_content_type', 'source_object_id')

    destination_content_type = models.ForeignKey(
        ContentType, related_name="corridor_destination_content_type", null=False, blank=False, limit_choices_to=limit, on_delete=models.DO_NOTHING)
    destination_object_id = models.PositiveIntegerField()
    destination_content_object = GenericForeignKey(
        'destination_content_type', 'destination_object_id')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Corridor"


class Grille(models.Model):
    corridor = models.ForeignKey('Corridor', on_delete=models.CASCADE)
    minimum_amount = models.DecimalField(max_digits=7, decimal_places=2)
    maximum_amount = models.DecimalField(max_digits=7, decimal_places=2)
    fee_type = models.CharField(max_length=5, choices=[
        (tag, tag.value) for tag in FeeType])
    fee = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = "Grille tarif."
