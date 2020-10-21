from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.contenttypes.models import ContentType
from tastypie.fields import ForeignKey
from apps.api.agent_api import AgentResource
from apps.transaction.models import Transaction
from django.conf.urls import url
from tastypie.utils import trailing_slash
import json
from apps.kyc.models import Customer

class TransactionHistoriqueResource(ModelResource):
    agent = ForeignKey(AgentResource, 'agent')

    class Meta:
        queryset = Transaction.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'transactions'
        filtering = {
            'transaction_type': ALL,
            'agent': ALL_WITH_RELATIONS,
            'status': ALL,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        excludes = ('code', 'resource_uri', 'destination_object_id', 'source_object_id', 'resource_uri', 'operation_amount')

    def determine_format(self, request):
        return 'application/json'

    def dehydrate_agent(self, bundle):
        return bundle.obj.agent.informations.username

    def dehydrate_destination_currency(self, bundle):
        return bundle.obj.destination_country.currency.name

    def dehydrate_destination_currency(self, bundle):
        return bundle.obj.destination_country.currency.name


    def dehydrate(self, bundle):
        bundle.data['source'] = self._transaction_source(bundle)
        bundle.data['destination'] = self._transaction_destination(bundle)
        bundle.data['currency'] = self._transaction_currency(bundle)

        return bundle

    def _transaction_source(self, bundle):
        if bundle.obj.source_content_type == ContentType.objects.get_for_model(Customer)\
                and bundle.obj.source_content_object:
            return'{0} {1}'.format(bundle.obj.source_content_object.informations.first_name,
                                   bundle.obj.source_content_object.informations.last_name)
        return None

    def _transaction_destination(self, bundle):
        if bundle.obj.destination_content_type == ContentType.objects.get_for_model(Customer)\
                and bundle.obj.destination_content_object:
            return'{0} {1}'.format(bundle.obj.destination_content_object.informations.first_name,
                                   bundle.obj.destination_content_object.informations.last_name)
        return None

    def _transaction_currency(self, bundle):
        return bundle.obj.grille.corridor.currency.name

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)
