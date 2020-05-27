
from tastypie.http import HttpUnauthorized, HttpForbidden
from apps.entity.repository.agent_repository import AgentRepository
from apps.entity.repository.entity_repository import EntityRepository
from django.contrib.auth.models import User
from apps.core.utils.http import create_jwt_token_for, get_request_token, decode_jwt_token
from apps.core.utils.string import verify_totp, generate_totp
from apps.services.tasks import sms_task


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
                bundle.data.update({'response_code': '000'})
                bundle.data.update(create_jwt_token_for(agent, 'agent_api_secret_key'))

                # TODO : Send sms asyncrhonously

                return tastypie.create_response(request, bundle)
            else:
                return tastypie.create_response(request, {'response_text': 'wrong password', 'response_code': '100'}, HttpForbidden)
        else:
            return tastypie.create_response(request, {'response_text': 'agent is not active', 'response_code': '100'}, HttpUnauthorized)
    except User.DoesNotExist:
        return tastypie.create_response(request, {'response_text': 'unknwonw user', 'response_code': '100'}, HttpForbidden)


def otp_authentication(tastypie, data, request):
    try:
        otp = data['otp']
        result = verify_totp(otp)
        if result is False:
            return tastypie.create_response(request, {'response_text': 'wrong OTP', 'response_code': '100'}, HttpUnauthorized)
        return tastypie.create_response(request, {'response_text': 'OK', 'response_code': '000'})
    except Exception:
        return tastypie.create_response(request, {'response_text': 'wrong OTP', 'response_code': '100'}, HttpForbidden)


def otp_renew(tastypie, request):
    try:
        agent_code = decode_jwt_token(get_request_token(request), 'agent_api_secret_key')
        agent = AgentRepository.fetch_by_code(agent_code.get('code'))
        otp = generate_totp()
        sms_task.run(agent.phone_number, otp)

        return tastypie.create_response(request, {'response_text': 'OK', 'response_code': '000'})
    except Exception:
        return tastypie.create_response(request, {'response_text': 'Unable to renew OTP', 'response_code': '100'}, HttpForbidden)
