from tastypie.resources import ModelResource
from tastypie.serializers import Serializer

from apps.shared.models.price import MotifEnvoi, SourceRevenu


class MotifEnvoiResource(ModelResource):
    class Meta:
        queryset = MotifEnvoi.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'shared/motifenvoi'
        serializer = Serializer(
            formats=['json', 'jsonp', 'xml', 'yaml', 'plist'])

    def determine_format(self, request):
        return 'application/json'


class SourceRevenuResource(ModelResource):
    class Meta:
        queryset = SourceRevenu.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'shared/sourcerevenu'
        serializer = Serializer(
            formats=['json', 'jsonp', 'xml', 'yaml', 'plist'])

    def determine_format(self, request):
        return 'application/json'
