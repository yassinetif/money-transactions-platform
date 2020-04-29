from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from shared.models.account import Account
from shared.models.country import Country, Currency
from django.contrib.contenttypes.fields import GenericRelation
from core.utils.string import random_code
from django.forms.models import model_to_dict
from enum import Enum


class EntityType(Enum):
    PROVIDER = 'PROVIDER'
    DISTRIBUTEUR = 'DISTRIBUTEUR'
    BANQUE = 'BANQUE'
    BUSINESS_PARTNER = 'BUSINESS_PARTNER'


class Entity(MPTTModel):
    code = models.CharField(
        unique=True,
        max_length=10,
        null=False,
        blank=False,
        default=random_code(6),
    )
    account_number = models.CharField(
        unique=True,
        max_length=9,
        null=False,
        blank=False,
        default=random_code(9),
    )
    category = models.CharField(max_length=30, choices=[
                                (tag.value, tag.value) for tag in EntityType], default='PROVIDER')
    brand_name = models.CharField(max_length=30, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    email = models.CharField(max_length=30, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    parent = TreeForeignKey("self", on_delete=models.CASCADE,
                            null=True, blank=True, related_name="children")
    accounts = GenericRelation(Account)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])

    class MPTTMeta:
        order_insertion_by = ["brand_name"]


class EntitySettings(models.Model):
    entity = models.ForeignKey('Entity', null=True, blank=True, on_delete=models.DO_NOTHING)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.DO_NOTHING)
    check_entity_balance = models.BooleanField(default=True, help_text='Check Entity balance before processing operation')
    overdraft_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0, help_text='Overdraft amount')

    def __str__(self):
        return self.entity

    class Meta:
        verbose_name = 'Entity setting'
