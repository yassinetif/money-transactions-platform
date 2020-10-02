from tastypie.resources import ModelResource, ALL
from apps.transaction.models import Transaction
from apps.transaction.controller.transaction_controller import create as create_transaction,\
    search as search_transaction, pay as pay_transaction, fee as transaction_fee, \
    get_entity_financial_situation, get_agent_transactions_stats
from django.conf.urls import url
from tastypie.utils import trailing_slash


class TransactionResource(ModelResource):

    class Meta:
        queryset = Transaction.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'transaction'
        filtering = {
            'transaction_type': ALL,
            'status': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    def determine_format(self, request):
        return 'application/json'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="api_create_transaction"),
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('search'), name="api_search_transaction"),
            url(r"^(?P<resource_name>%s)/pay%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('pay'), name="api_pay_transaction"),
            url(r"^(?P<resource_name>%s)/fee%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('fee'), name="api_fee_transaction"),
            url(r'^(?P<resource_name>%s)/agent/finance/situation%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('balance_situation'), name='api_balance_situation'),
            url(r'^(?P<resource_name>%s)/agent/stats%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('agent_transactions_stats'), name='api_agent_transactions_stat'),
        ]

    def create(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = create_transaction(self, payload, request)
        return response

    def search(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = search_transaction(self, payload, request)
        return response

    def pay(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = pay_transaction(self, payload, request)
        return response

    def fee(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = transaction_fee(self, payload, request)
        return response

    def balance_situation(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        response = get_entity_financial_situation(self, request)
        return response

    def agent_transactions_stats(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        response = get_agent_transactions_stats(self, request)
        return response

