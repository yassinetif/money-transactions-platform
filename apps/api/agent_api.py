from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie import fields
from entity.models import Agent
from entity.controller.agent_controller import login, logout
from django.conf.urls import url
from tastypie.utils import trailing_slash


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']


class AgentResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user',full=True)

    class Meta:
        queryset = Agent.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'entity/agent'
        filtering = {
            'slug': ALL,
            'user': ALL_WITH_RELATIONS,
            'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        response = login(self, request)
        return response

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        response = logout(self, request)
        return response
