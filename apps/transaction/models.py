from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from apps.entity.models.agent import Agent
from apps.entity.models.entity import Entity
from apps.shared.models.price import Grille, TransactionType
from apps.shared.models.price import MotifEnvoi, SourceRevenu
from apps.shared.models.account import Account
from apps.shared.models.country import Country
from apps.core.utils.string import random_code
from jsonfield import JSONField

from enum import Enum


class TransactionStatus(Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    SUSPENDED = 'SUSPENDED'


class TransactionCodePrefix(Enum):
    WORLD_REMIT = 'WR'
    YONNA = 'YN'


class Transaction(models.Model):

    number = models.CharField(
        max_length=11, default=random_code(10), unique=True, blank=False, null=False)
    code = models.CharField(
        max_length=11, default=random_code(9), unique=True, blank=False, null=False)

    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    operation_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    paid_amount = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
    limit = models.Q(app_label='entity', model='entity') \
        | models.Q(app_label='kyc', model='customer')
    paid_amount_in_destination_currency = models.DecimalField(
        max_digits=20, decimal_places=2, default=0)
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
    transaction_type = models.CharField(max_length=30, choices=[
        (tag.value, tag.value) for tag in TransactionType], default=TransactionType.CASH_TO_CASH.value)
    parent_transaction_number = models.CharField(
        max_length=11, default=random_code(10), blank=True, null=True)
    other_informations = models.TextField(blank=True, null=True)
    source_revenu = models.ForeignKey(
        SourceRevenu, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='transaction_source_revenu')
    motif_envoi = models.ForeignKey(
        MotifEnvoi, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='transaction_motif_envoi')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payload = JSONField(null=True)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        app_label = 'transaction'

    def __str__(self):
        return str(self.number)

    @property
    def paid_amount_with_currency_of_agent_operation(self):
        return '{0} {1}'.format(self.paid_amount, self.agent.entity.country.currency.iso)


class Operation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    transaction = models.ForeignKey(
        Transaction, null=False, blank=False, on_delete=models.DO_NOTHING)
    comment = models.TextField(_('Comment'), null=True, blank=True)
    balance_after_operation = models.ForeignKey(
        Account, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _('Operation detail')
        verbose_name_plural = _('Operations details')
        app_label = 'transaction'


class RevenuSharingResult(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    transaction = models.ForeignKey(
        Transaction, null=False, blank=False, on_delete=models.DO_NOTHING)
    entity = models.ForeignKey(
        Entity, null=False, blank=False, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = verbose_name_plural = _('Revenu Sharing result')
        app_label = 'transaction'
