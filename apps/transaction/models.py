from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from entity.models import Agent
from shared.models import Grille, Account, Country, TransactionType
from core.utils import random_code
from enum import Enum


class TransactionStatus(Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    SUSPENDED = 'SUSPENDED'


class Transaction(models.Model):

    number = models.CharField(
        max_length=11, default=random_code(10), unique=True, blank=False, null=False)
    code = models.CharField(
        max_length=11, default=random_code(8), unique=True, blank=False, null=False)

    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    paid_amount = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
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
    grille = models.ForeignKey(
        Grille, null=True, blank=True, on_delete=models.DO_NOTHING)

    source_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='transaction_source_country')
    destination_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='transaction_destination_country')

    status = models.CharField(max_length=20, choices=[
        (tag.value, tag.value) for tag in TransactionStatus], default=TransactionStatus.PENDING.value)

    transaction_type = models.CharField(max_length=20, choices=[
        (tag.value, tag.value) for tag in TransactionType], default=TransactionType.CASH_TO_CASH.value)

    parent_transaction_number = models.CharField(
        max_length=11, default=random_code(10), blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tranaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return str(self.number)


class Operation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    transaction = models.ForeignKey(
        Transaction, null=False, blank=False, on_delete=models.DO_NOTHING)
    comment = models.TextField('Commentaire', null=True, blank=True)
    balance_after_operation = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Operation detail'
        verbose_name_plural = 'Operatons details'
