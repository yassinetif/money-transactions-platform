from django.urls import path
from django.conf.urls import include
from tastypie.api import Api
from apps.api.agent_api import AgentResource
from apps.api.transaction_api import TransactionResource
from apps.api.customer_api import CustomerResource
from apps.api.shared_api import MotifEnvoiResource, SourceRevenuResource, CountryResource


v1_api = Api(api_name='v1')


# Agent
v1_api.register(AgentResource())

# Transaction
v1_api.register(TransactionResource())

# Customer
v1_api.register(CustomerResource())


# Shared
v1_api.register(MotifEnvoiResource())
v1_api.register(SourceRevenuResource())
v1_api.register(CountryResource())

urlpatterns = [
    path('api/', include(v1_api.urls)),
]
