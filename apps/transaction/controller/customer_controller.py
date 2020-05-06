
from .transaction_controller import _validate_transaction_payload, _get_agent_info,\
    _check_agent_balance, create_transaction, _debit_entity, insert_operation
from kyc.domain.customer_domain import get_customer_balance
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
        # TODO : activate_monnamon_card(payload)
        transaction = create_transaction(payload, agent)
        _debit_entity(agent, payload.get('paid_amount'))
        insert_operation(transaction)
        payload.update({'response_code': '000'})
        return tastypie.create_response(request, payload)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


def create_customer_with_wallet(tastypie, payload, request):
    try:
        data = payload.copy()
        data.update({'type': 'CREATION_WALLET'})
        _validate_transaction_payload(data)
        payload.update({'response_code': '000'})
        CustomerRepository.fetch_or_create_customer(payload)
        return tastypie.create_response(request, payload)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


def get_wallet_balance(tastypie, payload, request):
    try:
        data = payload.copy()
        data.update({'type': 'WALLET_BALANCE'})
        _validate_transaction_payload(data)
        customer = CustomerRepository.fetch_customer_by_phone_number(payload.get('phone_number'))
        balance = get_customer_balance(customer)
        payload.update({'response_code': '000', 'balance': balance})
        return tastypie.create_response(request, payload)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)
