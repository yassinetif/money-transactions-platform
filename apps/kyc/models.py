from django.db import models
from django.contrib.auth.models import User
from shared.models import Account, Country
from django.contrib.contenttypes.fields import GenericRelation


class Customer(models.Model):
    informations = models.OneToOneField(User, on_delete=models.CASCADE)
    accounts = GenericRelation(Account)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    identification_type = models.CharField(
        max_length=10, null=True, blank=True)
    identification_number = models.CharField(
        max_length=10, null=True, blank=True)
    issuer_country = models.ForeignKey(Country, on_delete=models.DO_NOTHING,null=True)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client"
