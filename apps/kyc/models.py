from django.db import models
from django.contrib.auth.models import User
from apps.shared.models.account import Account
from apps.shared.models.country import Country
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Customer(models.Model):
    informations = models.OneToOneField(User, on_delete=models.CASCADE)
    accounts = GenericRelation(Account)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    identification_type = models.CharField(
        max_length=10, null=True, blank=True)
    identification_number = models.CharField(
        max_length=10, null=True, blank=True)
    issuer_country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True, related_name='residence_country')
    identification_document_delivery_date = models.DateField(_('Document delivery date'), default=timezone.now)
    identification_document_expiry_date = models.DateField(_('Document expiry date'), default=timezone.now)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    status = models.BooleanField(default=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    relations = models.ManyToManyField('self', null=False, blank=False)

    class Meta:
        verbose_name = _('Client')
        app_label = 'kyc'

    def __str__(self):
        return '{0} {1}'.format(self.informations.first_name, self.informations.last_name)

    def __detail__(self):
        return {
            'first_name': self.informations.first_name,
            'last_name': self.informations.last_name,
            'phone_number': self.phone_number,
            'identification_number': self.identification_number,
        }

    @property
    def code(self):
        return self.informations.username


class Cartera(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    card_number = models.CharField(max_length=20, null=False, blank=False)
    card_identification_number = models.CharField(max_length=20, null=False, blank=False)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cartera')
        app_label = 'kyc'

    def __str__(self):
        return '{0}'.format(self.card_identification_number)
