from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from apps.transaction.models import Transaction
from tastypie.serializers import Serializer
from apps.transaction.controller.transaction_controller import create as create_transaction,\
    search as search_transaction, pay as pay_transaction, fee as transaction_fee
from django.conf.urls import url
from tastypie.utils import trailing_slash


class TransactionResource(ModelResource):

    class Meta:
        queryset = Transaction.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'transaction'
        filtering = {
            'slug': ALL,
            'user': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        serializer = Serializer(
            formats=['json', 'jsonp', 'xml', 'yaml', 'plist'])

    def determine_format(self, request):
        """
        Used to determine the desired format from the request.format
        attribute.
        """
        if (hasattr(request, 'format') and request.format in self._meta.serializer.formats):
            return self._meta.serializer.get_mime_for_format(request.format)
        return super(TransactionResource, self).determine_format(request)

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
