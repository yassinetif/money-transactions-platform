from django.urls import path
from django.conf.urls import include
from tastypie.api import Api
from api.agent_api import AgentResource

v1_api = Api(api_name='v1')


# Agent
v1_api.register(AgentResource())


urlpatterns = [
    path('api/', include(v1_api.urls)),
]
print(urlpatterns)
