from django.contrib import admin
from apps.kyc.models import Customer, Cartera
from django.utils.translation import ugettext_lazy as _


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'country', 'phone_number', 'identification_type',
                    'identification_number', 'issuer_country', 'address')
    filter_horizontal = ('relations',)
    search_fields = ('informations__first_name', 'informations__last_name', 'informations__username', )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def customer(self, obj):
        return' {} {} '.format(obj.informations.first_name, obj.informations.last_name)
    customer.allow_tags = True
    customer.short_description = _('Customer')

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
