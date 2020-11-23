from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from apps.kyc.models import Customer

from django.conf.urls import url
from tastypie.utils import trailing_slash
from apps.transaction.controller.customer_controller import create_customer_with_card,\
    create_customer_with_wallet, get_wallet_balance, wallet_login, define_wallet_password, customer_beneficiaries,\
    customer_info


class CustomerResource(ModelResource):

    class Meta:
        queryset = Customer.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'customer'
        filtering = {
            'slug': ALL,
            'user': ALL_WITH_RELATIONS,
            'relations': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    def determine_format(self, request):
        return 'application/json'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/card/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('activate_card'), name="api_activate_card"),
            url(r"^(?P<resource_name>%s)/wallet/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create_wallet'), name="api_create_wallet"),
            url(r"^(?P<resource_name>%s)/wallet/balance%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('wallet_balance'), name="api_wallet_balance"),
            url(r"^(?P<resource_name>%s)/wallet/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('wallet_login'), name="api_wallet_login"),
            url(r"^(?P<resource_name>%s)/wallet/password%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('wallet_password'), name="api_wallet_password"),
            url(r"^(?P<resource_name>%s)/wallet/beneficiaries%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('beneficiaries'), name="api_beneficiaries"),
            url(r"^(?P<resource_name>%s)/info%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('info'), name="api_customer_info"),
        ]

    def activate_card(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = create_customer_with_card(self, payload, request)
        return response

    def create_wallet(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = create_customer_with_wallet(self, payload, request)
        return response

    def wallet_balance(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = get_wallet_balance(self, payload, request)
        return response

    def wallet_login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = wallet_login(self, payload, request)
        return response

    def wallet_password(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = define_wallet_password(self, payload, request)
        return response

    def beneficiaries(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        phone_number = request.GET['phone_number']
        response = customer_beneficiaries(self, phone_number, request)
        return response

    def info(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        phone_number = request.GET['phone_number']
        response = customer_info(self, phone_number, request)
        return response
