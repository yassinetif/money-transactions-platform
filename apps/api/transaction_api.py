from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from transaction.models import Transaction
from tastypie.serializers import Serializer
from transaction.controller.transaction_controller import create as create_transaction
from django.conf.urls import url
from tastypie.utils import trailing_slash
import json
import logging

logger = logging.getLogger(__name__)



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
        if (hasattr(request, 'format') and
                request.format in self._meta.serializer.formats):
            return self._meta.serializer.get_mime_for_format(request.format)
        return super(TransactionResource, self).determine_format(request)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="api_create_transaction"),
        ]

    def create(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        payload = self.deserialize(request, request.body)
        response = create_transaction(self, payload, request)
        return response
