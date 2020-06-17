from django.contrib import admin
from apps.kyc.models import Customer, Cartera


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('informations', 'country', 'phone_number', 'identification_type',
                    'identification_number', 'issuer_country', 'address')
    filter_horizontal = ('relations',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(CustomerAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


admin.site.register(Customer, CustomerAdmin)


class CarteraAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_number', 'card_identification_number',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Cartera, CarteraAdmin)
