from django.db import models
from django.contrib.auth.models import User
from shared.models.account import Account
from shared.models.country import Country
from django.contrib.contenttypes.fields import GenericRelation
import datetime


class Customer(models.Model):
    informations = models.OneToOneField(User, on_delete=models.CASCADE)
    accounts = GenericRelation(Account)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    identification_type = models.CharField(
        max_length=10, null=True, blank=True)
    identification_number = models.CharField(
        max_length=10, null=True, blank=True)
    issuer_country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True)
    identification_document_deleivery_date = models.DateField(" Document deleivery date", default=datetime.date.today)
    identification_document_expiry_date = models.DateField("Document expiry date", default=datetime.date.today)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client"

    def __str__(self):
        return '{0} {1}'.format(self.informations.first_name, self.informations.last_name)


class Cartera(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    card_number = models.CharField(max_length=20, null=False, blank=False)
    card_identification_number = models.CharField(max_length=20, null=False, blank=False)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cartera"

    def __str__(self):
        return '{0}'.format(self.card_identification_number)
