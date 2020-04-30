from django.contrib import admin
from kyc.models import Customer, Cartera


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('informations', 'phone_number', 'identification_type',
                    'identification_number', 'issuer_country', 'identification_document_deleivery_date',
                    'identification_document_expiry_date', 'address')


admin.site.register(Customer, CustomerAdmin)


class CarteraAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_number', 'card_identification_number',)


admin.site.register(Cartera, CarteraAdmin)
