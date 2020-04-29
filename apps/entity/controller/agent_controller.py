
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
                bundle.data.update({'reponse_code': '000'})

                return tastypie.create_response(request, bundle)
            else:
                return tastypie.create_response(request, {'response_text': 'wrong password', 'response_code': '100'}, HttpForbidden)
        else:
            return tastypie.create_response(request, {'response_text': 'agent is not active', 'response_code': '100'}, HttpUnauthorized)
    except User.DoesNotExist:
        return tastypie.create_response(request, {'response_text': 'unknwonw user', 'response_code': '100'}, HttpForbidden)
