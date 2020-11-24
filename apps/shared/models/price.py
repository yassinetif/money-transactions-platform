from django.db import models
from apps.shared.models.country import Country, Currency
from django.utils.translation import ugettext_lazy as _
from enum import Enum
from apps.core.utils.string import validate_calculation_expression
from django.utils.text import slugify
class TransactionType(Enum):
    CASH_TO_CASH = 'CASH_TO_CASH'
    CASH_TO_WALLET = 'CASH_TO_WALLET'
    WALLET_TO_CASH = 'WALLET_TO_CASH'
    WALLET_TO_WALLET = 'WALLET_TO_WALLET'
    RETRAIT_CASH = 'RETRAIT_CASH'
    ACTIVATION_CARTE = 'ACTIVATION_CARTE'
    CREATION_WALLET = 'CREATION_WALLET'
    CREDIT_COMPTE_ENTITE = 'CREDIT_COMPTE_ENTITE'
    DEBIT_COMPTE_ENTITE = 'DEBIT_COMPTE_ENTITE'
    CASH_TO_BANK_ACCOUNT = 'CASH_TO_BANK_ACCOUNT'
    WALLET_TO_BANK_ACCOUNT = 'WALLET_TO_BANK_ACCOUNT'
    BATCH = 'BATCH'
    RECOUVREMENT = 'RECOUVREMENT'


AGENT_TRANSACTIONS = ['CASH_TO_CASH', 'CASH_TO_WALLET', 'RETRAIT_CASH', 'ACTIVATION_CARTE', 'CREDIT_COMPTE_ENTITE', 'DEBIT_COMPTE_ENTITE', 'CASH_TO_BANK_ACCOUNT']
WALLET_TRANSACTIONS = ['WALLET_TO_CASH', 'CREATION_WALLET', 'WALLET_TO_WALLET', 'WALLET_TO_BANK_ACCOUNT']

class FeeType(Enum):
    CONST = 'CONSTANTE'
    PERCENT = 'PERCENTAGE'


class Sharing(models.Model):
    calculation_expression = models.CharField(max_length=200,
                                              validators=[validate_calculation_expression],
                                              help_text='FEE/2=>PROVIDER:0.2:+;BANQUE:0.4:-')
    is_standard = models.BooleanField(help_text=_('Tell if this is the standard sharing to use for this corridor'), default=False)
    corridor = models.ForeignKey('Corridor', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('Revenue Sharing')
        app_label = 'shared'


class Corridor(models.Model):

    name = models.CharField(max_length=30, null=False, blank=False)
    limit = models.Q(app_label='entity', model='entity') \
        | models.Q(app_label='shared', model='country')

    transaction_type = models.CharField(max_length=30, choices=[
        (tag.value, tag.value) for tag in TransactionType])

    source_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='source_country')
    destination_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='destination_country')
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Corridor')
        app_label = 'shared'


class Grille(models.Model):
    corridor = models.ForeignKey('Corridor', on_delete=models.CASCADE)
    minimum_amount = models.DecimalField(max_digits=15, decimal_places=2)
    maximum_amount = models.DecimalField(max_digits=15, decimal_places=2)
    fee_type = models.CharField(max_length=15, choices=[
        (tag.value, tag.value) for tag in FeeType])
    fee = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = _('Pricing')
        app_label = 'shared'


class MotifEnvoi(models.Model):
    code = models.CharField(
        unique=True,
        max_length=10,
        null=False,
        blank=False,
    )
    libelle = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = _('Motif Envoi')
        app_label = 'shared'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.code = slugify(self.libelle)
        super(MotifEnvoi, self).save(*args, **kwargs)


class SourceRevenu(models.Model):
    code = models.CharField(
        unique=True,
        max_length=10,
        null=False,
        blank=False,
    )
    libelle = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = _('Source de revenus')
        app_label = 'shared'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.code = slugify(self.libelle)
        super(SourceRevenu, self).save(*args, **kwargs)
