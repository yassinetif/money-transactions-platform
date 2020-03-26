
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from entity.repository.agent_repository import AgentRepository


def login(tastypie, request):
    data = tastypie.deserialize(request, request.raw_post_data, format=request.META.get(
        'CONTENT_TYPE', 'application/json'))

    username = data.get('username', '')
    password = data.get('password', '')
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            agent = AgentRepository.fetch_by_user(user)
            bundle = tastypie.build_bundle(obj=agent, request=request)
            bundle = tastypie.full_dehydrate(bundle)
            return tastypie.create_response(request, bundle)
        else:
            return tastypie.create_response(request, {
                'success': False,
                'reason': 'disabled',
            }, HttpForbidden)
    else:
        return tastypie.create_response(request, {
            'success': False,
            'reason': 'incorrect',
        }, HttpUnauthorized)


def logout(tastypie, request):
    if request.user and request.user.is_authenticated():
        logout(request)
        return tastypie.create_response(request, {'success': True})
    else:
        return tastypie.create_response(request, {'success': False}, HttpUnauthorized)
