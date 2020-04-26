from django.contrib import admin
from kyc.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('informations', 'phone_number', 'identification_type',
                    'identification_number', 'issuer_country', 'address')


admin.site.register(Customer, CustomerAdmin)
