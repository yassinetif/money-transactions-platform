
from tastypie.http import HttpUnauthorized, HttpForbidden
from entity.repository.agent_repository import AgentRepository
from entity.repository.entity_repository import EntityRepository
from django.contrib.auth.models import User


def login(tastypie, data, request):

    username = data['username']
    password = data['password']

    try:
        user = User.objects.get(username=username)
        if user and user.is_active:
            result = user.check_password(password)
            if result:
                agent = AgentRepository.fetch_by_user(user)
                bundle = tastypie.build_bundle(obj=agent, request=request)
                bundle = tastypie.full_dehydrate(bundle)

                entity = EntityRepository.fetch_by_agent(agent)
                bundle.data.update({'entity': entity})

                return tastypie.create_response(request, bundle)
            else:
                return tastypie.create_response(request, {'reason': 'wrong password'}, HttpForbidden)
        else:
            return tastypie.create_response(request, {'reason': 'user is not active'}, HttpUnauthorized)
    except User.DoesNotExist:
        return tastypie.create_response(request, {'reason': 'unknown user'}, HttpForbidden)
