import json
import requests
import datetime
import jwt
from apps.shared.global_config import GLOBAL_CONFIG as global_config
from apps.core.errors import ApiAuthenticationException, NetworkException


def post_simple_json_request(url, data, headers_info=None):
    try:
        headers = {'Content-Type': 'application/json'}
        if headers_info:
            headers.update(headers_info)
        response = requests.post(url, data=json.dumps(data), headers=headers).json()
    except NetworkException as e:
        raise NetworkException(str(e), 'unable to post data to URL')
    return response


def get_request_token(request=None):
    try:
        return request.META.get('HTTP_AUTHORIZATION').split(' ')[1] or request.GET.get('token')
    except Exception as e:
        raise ApiAuthenticationException(str(e), 'invalid authorization token')

def create_jwt_token_for(obj, secret_key):
    payload = {
        'id': obj.pk,
        'code': obj.code,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    token = {'token': jwt.encode(payload, global_config.get(secret_key))}

    return token


def decode_jwt_token(token, secret_key):
    try:
        payload = jwt.decode(token, global_config.get(secret_key))
        return payload
    except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError) as e:
        raise ApiAuthenticationException(str(e), 'invalid authorization token')
