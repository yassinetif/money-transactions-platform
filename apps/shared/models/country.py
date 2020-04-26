from django.db import models
from django_countries.fields import CountryField


class Country(models.Model):
    iso = CountryField()
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.iso.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
