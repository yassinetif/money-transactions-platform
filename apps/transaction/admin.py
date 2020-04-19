from django.contrib import admin
from transaction.models import Transaction, Operation


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'number', 'code', 'agent', 'entity', 'amount',
                    'paid_amount', 'transaction_fee', 'source_country', 'destination_country', 'status', 'created')
    list_filter = ('created', 'status',)

    def transaction_fee(self, obj):
        return obj.grille.fee
    transaction_fee.allow_tags = True
    transaction_fee.short_description = 'Frais'


    def entity(self, obj):
        return obj.agent.entity.brand_name
    entity.allow_tags = True
    entity.short_description = 'Entity'


admin.site.register(Transaction, TransactionAdmin)


class OperationAdmin(admin.ModelAdmin):
    list_display = ('created', '_balance_after_operation',
                    'comment', 'transaction', 'transaction_type')

    def _balance_after_operation(self, obj):
        return obj.transaction.agent.entity.accounts.last().balance
    _balance_after_operation.allow_tags = True
    _balance_after_operation.short_description = 'Balance after operation'

    def transaction_type(self, obj):
        return obj.transaction.transaction_type
    transaction_type.allow_tags = True
    transaction_type.short_description = 'Type'


admin.site.register(Operation, OperationAdmin)
