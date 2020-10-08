from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.fields import ForeignKey
from apps.api.agent_api import AgentResource
from apps.transaction.models import Transaction
from django.conf.urls import url
from tastypie.utils import trailing_slash


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
        excludes = ('code', 'resource_uri')

    def determine_format(self, request):
        return 'application/json'

    def dehydrate_agent(self, bundle):
        return bundle.obj.agent.informations.username

    def dehydrate_destination_currency(self, bundle):
        return bundle.obj.destination_country.currency.name

    def dehydrate_destination_currency(self, bundle):
        return bundle.obj.destination_country.currency.name

    
    def alter_list_data_to_serialize(self, request, data):
        data['page']['objects'] = {'your_data': True}
        return data

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)
