
from core.utils.http import decode_jwt_token

def agent_code_required(function):
    def modified_function(payload, token):
        decoded_payload = decode_jwt_token(token, 'agent_api_secret_key')
        payload.update({'agent': {'code': decoded_payload.get('code')}})
        return function(payload, token)
    return modified_function
