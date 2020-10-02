from django.urls import path
from django.conf.urls import include
from tastypie.api import Api
from apps.api.agent_api import AgentResource
from apps.api.entity_api import EntityResource
from apps.api.transaction_api import TransactionResource
from apps.api.transaction_historique_api import TransactionHistoriqueResource
from apps.api.customer_api import CustomerResource
from apps.api.shared_api import MotifEnvoiResource, SourceRevenuResource, CountryResource


v1_api = Api(api_name='v1')

# Entity
v1_api.register(EntityResource())

# Agent
v1_api.register(AgentResource())

# Transaction & historique
v1_api.register(TransactionResource())
v1_api.register(TransactionHistoriqueResource())

# Customer
v1_api.register(CustomerResource())


# Shared
v1_api.register(MotifEnvoiResource())
v1_api.register(SourceRevenuResource())
v1_api.register(CountryResource())

urlpatterns = [
    path('api/', include(v1_api.urls)),
]
