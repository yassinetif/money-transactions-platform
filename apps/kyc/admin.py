from django.contrib import admin
from apps.kyc.models import Customer, Cartera


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('informations', 'country', 'phone_number', 'identification_type',
                    'identification_number', 'issuer_country', 'address')


admin.site.register(Customer, CustomerAdmin)


class CarteraAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_number', 'card_identification_number',)


admin.site.register(Cartera, CarteraAdmin)
