from django.db import models
from django.contrib.auth.models import User
from shared.models import Account
from django.contrib.contenttypes.fields import GenericRelation


class Customer(models.Model):
    informations = models.OneToOneField(User, on_delete=models.CASCADE)
    accounts = GenericRelation(Account)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agent"
