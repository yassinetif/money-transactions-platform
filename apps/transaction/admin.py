from django.contrib import admin
from django.shortcuts import render
from transaction.models import Transaction, Operation
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'number', 'code', 'agent', 'entity', 'transaction_amount',
                    'transaction_paid_amount', 'transaction_fee', 'fee_currency', 'source_country', 'destination_country', 'status', 'created')
    list_filter = ('created', 'status',)
    actions = ['update_status']

    def transaction_fee(self, obj):
        return obj.grille.fee
    transaction_fee.allow_tags = True
    transaction_fee.short_description = 'Frais'

    def fee_currency(self, obj):
        return obj.grille.corridor.currency
    fee_currency.allow_tags = True
    fee_currency.short_description = 'Frais'

    def entity(self, obj):
        return obj.agent.entity.brand_name
    entity.allow_tags = True
    entity.short_description = 'Entity'

    def transaction_amount(self, obj):
        return '{} {} '.format(obj.amount, obj.source_country.currency.iso)
    transaction_amount.allow_tags = True
    transaction_amount.short_description = 'Transaction amount'

    def transaction_paid_amount(self, obj):
        return '{} {} '.format(obj.paid_amount, obj.source_country.currency.iso)
    transaction_paid_amount.allow_tags = True
    transaction_paid_amount.short_description = 'Paid amount'

    def update_status(self, request, queryset):
        return render(request,
                      'admin/order_intermediate.html',
                      context={})

    update_status.short_description = "Update status"


admin.site.register(Transaction, TransactionAdmin)


class OperationAdmin(admin.ModelAdmin):
    list_display = ('created', 'balance_after_operation', 'transaction', 'transaction_type')

    def transaction_type(self, obj):
        return obj.transaction.transaction_type
    transaction_type.allow_tags = True
    transaction_type.short_description = 'Type'


admin.site.register(Operation, OperationAdmin)
