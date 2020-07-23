from django.db import models
from django import forms
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from apps.shared.models.account import Account
from apps.shared.models.country import Country
from django.contrib.contenttypes.fields import GenericRelation
from apps.core.utils.string import random_code
from django.forms.models import model_to_dict
from apps.core.utils.string import entity_logo_directory_path
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
    is_payer = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=entity_logo_directory_path, blank=True)

    def __str__(self):
        return self.brand_name

    def to_dict(self):
        return model_to_dict(self, fields=[field.name for field in self._meta.fields if field.name != 'secret_key'])

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.code = random_code(6)
            self.account_number = '{}{}'.format(self.country.iso.code, random_code(9))
        super(Entity, self).save(*args, **kwargs)
        self.initialize_accounts()

    def initialize_accounts(self):
        if self.accounts.count() == 0:
            Account.objects.create(content_object=self,
                                   category='PRINCIPAL', balance=0)
            Account.objects.create(content_object=self,
                                   category='COMMISSION', balance=0)

    class MPTTMeta:
        order_insertion_by = ["brand_name"]

    class Meta:
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')
        app_label = 'entity'


class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        exclude = ('code', 'account_number')


class EntitySettings(models.Model):
    entity = models.ForeignKey('Entity', null=True, blank=True, on_delete=models.DO_NOTHING)
    check_entity_balance = models.BooleanField(default=True, help_text=_('Check Entity balance before processing operation'))
    overdraft_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text=_('Overdraft amount'))

    def __str__(self):
        return self.entity.brand_name

    class Meta:
        verbose_name = _('Entity setting')
        verbose_name_plural = _('Entities settings')
        app_label = 'entity'
