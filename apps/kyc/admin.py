from django.contrib import admin
from apps.kyc.models import Customer, Cartera


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('informations', 'country', 'phone_number', 'identification_type',
                    'identification_number', 'issuer_country', 'address')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Customer, CustomerAdmin)


class CarteraAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_number', 'card_identification_number',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Cartera, CarteraAdmin)
