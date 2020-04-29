from django.db import models
from django_countries.fields import CountryField


class Currency(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    iso = models.CharField(null=False, blank=False, max_length=3)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.iso

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"


class Country(models.Model):
    iso = CountryField()
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    currency = models.ForeignKey('Currency', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.iso.code

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Change(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    source_currency = models.ForeignKey('Currency', null=True, blank=True, related_name='source_currency', on_delete=models.DO_NOTHING)
    destination_currency = models.ForeignKey('Currency', null=True, blank=True, related_name='destination_currency', on_delete=models.DO_NOTHING)
    parity = models.DecimalField(max_digits=7, decimal_places=2, default=1)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Change"
        verbose_name_plural = "Changes"
