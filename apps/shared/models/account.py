from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from enum import Enum


class AccountType(Enum):
    PRINCIPAL = 1
    COMMISSION = 2


class Account(models.Model):
    limit = models.Q(app_label='entity', model='entity') \
        | models.Q(app_label='kyc', model='customer')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    category = models.CharField(max_length=30, choices=[
                                (tag.value, tag.value) for tag in AccountType],default=AccountType.PRINCIPAL)
    balance = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.category)

    class Meta:
        verbose_name = "Account"
