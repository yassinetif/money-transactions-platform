from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from tastypie.serializers import Serializer
from apps.entity.models.agent import Agent
from apps.entity.controller.agent_controller import login as agent_login,\
    otp_authentication as otp_auth, otp_renew as otp_renew_code
from django.conf.urls import url
from tastypie.utils import trailing_slash


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_superuser']


class AgentResource(ModelResource):

    class Meta:
        queryset = Agent.objects.all()
        list_allowed_methods = ['get', 'post', 'options']
        detail_allowed_methods = ['get', 'post', 'put', 'delete','options']
        resource_name = 'entity/agent'
        filtering = {
            'slug': ALL,
            'code': ALL,
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
        return super(AgentResource, self).determine_format(request)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/login/otp%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('otp_authentication'), name='api_otp_authentication'),
            url(r'^(?P<resource_name>%s)/login/otp/renew%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('otp_renew'), name='api_otp_renew'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)
        response = agent_login(self, data, request)
        return response

    def otp_authentication(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        response = otp_auth(self, request)
        return response

    def otp_renew(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        response = otp_renew_code(self, request)
        return response
