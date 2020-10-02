from tastypie.resources import ModelResource, ALL
from apps.transaction.models import Transaction
from apps.transaction.controller.transaction_controller import create as create_transaction,\
    search as search_transaction, pay as pay_transaction, fee as transaction_fee, \
    get_entity_financial_situation, get_agent_transactions_stats
from django.conf.urls import url
from tastypie.utils import trailing_slash


class TransactionHistoriqueResource(ModelResource):

    class Meta:
        queryset = Transaction.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'transactions'
        filtering = {
            'transaction_type': ALL,
            'status': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    def determine_format(self, request):
        return 'application/json'

