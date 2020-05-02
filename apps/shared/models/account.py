from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from enum import Enum


class AccountType(Enum):
    PRINCIPAL = 'PRINCIPAL'
    COMMISSION = 'COMMISSION'


class Account(models.Model):
    limit = models.Q(app_label='entity', model='entity') \
        | models.Q(app_label='kyc', model='customer')
    content_type = models.ForeignKey(
        ContentType, on_delete=models.DO_NOTHING, limit_choices_to=limit, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()
    category = models.CharField(max_length=30, choices=[
                                (tag.value, tag.value) for tag in AccountType], default=AccountType.PRINCIPAL.value)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.balance)

    class Meta:
        verbose_name = "Account"
