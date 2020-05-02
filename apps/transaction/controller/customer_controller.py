
from .transaction_controller import _validate_transaction_payload, _get_agent_info,\
    _check_agent_balance, create_transaction, _debit_entity, insert_operation
from tastypie.http import HttpUnauthorized, HttpForbidden
from kyc.repository.kyc_repository import CustomerRepository
from core.errors import CoreException
from marshmallow import ValidationError

def create_customer_with_card(tastypie, payload, request):
    try:
        payload.update({'type': 'ACTIVATION_CARTE'})
        _validate_transaction_payload(payload.copy())
        agent = _get_agent_info(payload)
        _check_agent_balance(agent, payload)
        transaction = create_transaction(payload, agent)
        _debit_entity(agent, payload.get('paid_amount'))
        insert_operation(transaction)
        response = payload.update({'response_code': '000'})
        return tastypie.create_response(request, response)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


def create_customer_with_wallet(tastypie, payload, request):
    try:
        data = payload.copy()
        data.update({'type': 'CREATION_WALLET'})
        _validate_transaction_payload(payload.copy())
        response = payload.update({'response_code': '000'})
        CustomerRepository.fetch_or_create_customer(payload)
        return tastypie.create_response(request, response)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)
