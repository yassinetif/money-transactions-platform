
from apps.core.utils.http import decode_jwt_token

def agent_code_required(function):
    def modified_function(payload, token):
        print (payload) # Print de vérification à enlever
        print (token) # Print de vérification à enlever
        decoded_payload = decode_jwt_token(token, 'agent_api_secret_key')
        payload.update({'agent': {'code': decoded_payload.get('code')}})
        return function(payload, token)
    return modified_function


""" Optimisation du code pour qu'on puisse utiliser la fonction modified_function dans la fonction ci-dessous aussi
def modified_function(function, payload, token, var, api):
    decoded_payload = decode_jwt_token(token, api)
    payload.update({var: {'code': decoded_payload.get('code')}})
    return function(payload, token)

def agent_code_required():
    return modified_function(payload, token, 'agent', 'agent_api_secret_key')
"""

def customer_code_required(function):
    def modified_function(payload, token):
        decoded_payload = decode_jwt_token(token, 'wallet_api_secret_key')
        payload.update({'code': decoded_payload.get('code')}) # Il ne manque pas un {customer:{'code':...} par hasard??
        return function(payload, token)
    return modified_function

