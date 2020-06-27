from django.contrib import admin
from apps.transaction.models import Transaction, Operation, RevenuSharingResult
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from apps.kyc.models import Customer

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'code', 'agent', 'entity', 'transaction_amount',
                    'transaction_paid_amount', 'transaction_fee', 'source',
                    'source_country', 'beneficiary', 'destination_country', 'other_informations', 'status', 'created')
    list_filter = ('created', 'status',)
    search_fields = ['agent__entity__brand_name','transaction_type','code','source_country__iso','destination_country__iso']
    date_hierarchy = 'created'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def transaction_fee(self, obj):
        return' {} {} '.format(obj.grille.fee, obj.grille.corridor.currency)
    transaction_fee.allow_tags = True
    transaction_fee.short_description = _('Fee')

    def entity(self, obj):
        return obj.agent.entity.brand_name
    entity.allow_tags = True
    entity.short_description = _('Entity')

    def transaction_amount(self, obj):
        return '{} {} '.format(obj.amount, obj.source_country.currency.iso)
    transaction_amount.allow_tags = True
    transaction_amount.short_description = _('Transaction amount')

    def transaction_paid_amount(self, obj):
        return '{} {} '.format(obj.paid_amount, obj.source_country.currency.iso)
    transaction_paid_amount.allow_tags = True
    transaction_paid_amount.short_description = _('Paid amount')

    def source(self, obj):
        if obj.source_content_type == ContentType.objects.get_for_model(Customer)\
                and obj.source_content_object:
            return '{0} {1}'.format(obj.source_content_object.informations.first_name, obj.source_content_object.informations.last_name)
    source.allow_tags = True
    source.short_description = 'Source'

    def beneficiary(self, obj):
        if obj.destination_content_type == ContentType.objects.get_for_model(Customer)\
                and obj.source_content_object:
            return '{0} {1}'.format(obj.destination_content_object.informations.first_name, obj.destination_content_object.informations.last_name)
    beneficiary.allow_tags = True
    beneficiary.short_description = 'Benef.'


admin.site.register(Transaction, TransactionAdmin)


class OperationAdmin(admin.ModelAdmin):
    list_display = ('created', 'balance_after_operation', 'transaction', 'transaction_type')

    def transaction_type(self, obj):
        return obj.transaction.transaction_type
    transaction_type.allow_tags = True
    transaction_type.short_description = _('Type')


admin.site.register(Operation, OperationAdmin)


class RevenuSharingResultAdmin(admin.ModelAdmin):
    list_display = ('created', 'entity', 'transaction', 'transaction_type', 'amount')
    search_fields = ('transaction__number',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def transaction_type(self, obj):
        return obj.transaction.transaction_type
    transaction_type.allow_tags = True
    transaction_type.short_description = _('Type')


admin.site.register(RevenuSharingResult, RevenuSharingResultAdmin)
