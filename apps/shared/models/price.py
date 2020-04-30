from django.db import models
from django.core.exceptions import ValidationError
from shared.models.country import Country, Currency
from enum import Enum
from decimal import Decimal


class TransactionType(Enum):
    CASH_TO_CASH = 'CASH_TO_CASH'
    RETRAIT_CASH = 'RETRAIT_CASH'


class FeeType(Enum):
    CONST = 'CONSTANTE'
    PERCENT = 'PERCENTAGE'


def validate_calculation_expression(expression):
    try:
        sharing_expression = expression.split('->')[1]
        for sharing_plan in sharing_expression.split("#"):
            revenue = 0
            for _s in sharing_plan.split(';'):
                expr = _s.split(':')
                sens = expr[2]
                if sens == 'DEBIT':
                    revenue -= Decimal(expr[1])
                else:
                    revenue += Decimal(expr[1])
            if revenue != 1:
                raise ValidationError('La somme doit être = 1 . Valeur {0}'.format(revenue))
    except Exception as err:
        raise ValidationError(err)

class Sharing(models.Model):
    calculation_expression = models.CharField(max_length=200,
                                              validators=[validate_calculation_expression],
                                              help_text='FRAIS/2->PROVIDER:0.2:CREDIT;BANQUE:0.4:CREDIT')
    corridor = models.ForeignKey('Corridor', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Revenue Sharing"


class Corridor(models.Model):

    name = models.CharField(max_length=30, null=False, blank=False)
    limit = models.Q(app_label='entity', model='entity') \
        | models.Q(app_label='shared', model='country')

    transaction_type = models.CharField(max_length=20, choices=[
        (tag.value, tag.value) for tag in TransactionType])

    source_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='source_country')
    destination_country = models.ForeignKey(
        Country, null=True, blank=True, on_delete=models.DO_NOTHING, related_name='destination_country')
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Corridor"


class Grille(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    corridor = models.ForeignKey('Corridor', on_delete=models.CASCADE)
    minimum_amount = models.DecimalField(max_digits=7, decimal_places=2)
    maximum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_type = models.CharField(max_length=15, choices=[
        (tag.value, tag.value) for tag in FeeType])
    fee = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = "Grille tarif."
