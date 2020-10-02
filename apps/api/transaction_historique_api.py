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

    def determine_format(self, request):
        return 'application/json'

    def dehydrate_agent(self, bundle):
        import pdb; pdb.set_trace()
        bundle.data['agent'] = 'TEST'

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)
