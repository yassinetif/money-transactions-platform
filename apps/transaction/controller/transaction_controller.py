
from decimal import Decimal
import json
from core.errors import CoreException, CustomerException
from core.utils.http import get_request_token

from core.utils.string import convert_snake_to_camel_case
from marshmallow import ValidationError
from importlib import import_module
from core.utils.validator import SearchTransactionCodeValidator, FeeValidator
from tastypie.http import HttpUnauthorized, HttpForbidden
from entity.repository.agent_repository import AgentRepository
from kyc.repository.kyc_repository import CustomerRepository
from kyc.domain.customer_domain import check_customer_balance, get_customer_balance, debit_customer_account
from entity.domain.entity_domain import check_entity_balance, get_entity_balance_by_agent
from transaction.domain.transaction_domain import debit_entity_account, create_transaction, \
    insert_operation, search_transaction, pay_transaction,\
    credit_entity_account, calculate_transaction_fee
from transaction.decorator.transaction_decorator import agent_code_required
from shared.models.price import AGENT_TRANSACTIONS


def _get_validator_class(transaction_type):
    validator = convert_snake_to_camel_case(transaction_type)
    module = import_module('core.utils.validator')
    klass = getattr(module, '{}Validator'.format(validator))
    return klass()

def _validate_transaction_payload(payload):
    try:
        transaction_type = payload.pop('type')
        validator_klass = _get_validator_class(transaction_type)
        validator_klass.load(payload)
    except ValidationError as err:
        raise ValidationError(str(err))
    except KeyError:
        raise ValidationError('please specify transaction type')


def _dump_transaction_payload(transaction):
    try:
        transaction_type = transaction.grille.corridor.transaction_type
        validator_klass = _get_validator_class(transaction_type)
        return json.loads(validator_klass.dumps(transaction))

    except ValidationError as err:
        raise ValidationError(str(err))


def _validate_search_transaction_by_code_payload(payload):
    try:
        SearchTransactionCodeValidator().load(payload)
    except ValidationError as err:
        raise ValidationError(str(err))

def _get_agent_info(payload):
    return AgentRepository.fetch_by_code(payload.get('agent').get('code'))

def _get_customer_info(payload):
    return CustomerRepository.fetch_customer_by_phone_number(payload.get('source_content_object').get('phone_number'))


def _check_agent_balance(agent, payload):
    if not check_entity_balance(agent, payload.get('paid_amount')):
        raise CoreException('agent does not have enough balance', 'agent does not have enough balance')


def _check_customer_balance(customer, payload):
    if not check_customer_balance(customer, payload.get('paid_amount')):
        raise CustomerException('customer does not have enough balance', 'customer does not have enough balance')


def _debit_entity(agent, amount, fee=0):
    last_balance = get_entity_balance_by_agent(agent)
    debit_entity_account(agent, last_balance, amount)


def _debit_customer(customer, amount, fee=0):
    last_balance = get_customer_balance(customer)
    debit_customer_account(customer, last_balance, amount)


def _credit_entity(agent, amount):
    last_balance = get_entity_balance_by_agent(agent)
    credit_entity_account(agent, last_balance, amount)


def _addtitional_transactions_informations(transaction, payload):
    info = {'transaction_number': transaction.number,
            'receipt_code': transaction.code}
    payload.update(info)
    return payload


def _addtitional_customer_informations(payload):
    customer = CustomerRepository.fetch_customer_by_phone_number(
        payload.get('phone_number'))
    info = {'first_name': customer.informations.first_name,
            'last_name': customer.informations.last_name}
    payload.update(info)
    return payload


def fee(tastypie, payload, request):
    try:
        FeeValidator().load(payload)
        agent = _get_agent_info(payload)
        total_fee = calculate_transaction_fee(payload, agent.entity)
        response = {'response_code': '000', 'response_text': total_fee}
        return tastypie.create_response(request, response)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


def create(tastypie, payload, request):
    try:
        _validate_transaction_payload(payload.copy())
        token = get_request_token(request)
        transaction_type = payload.get('type')
        if transaction_type in AGENT_TRANSACTIONS:
            transaction = _create_agent_transaction(payload, token)
            print ('enfin ici', transaction)
        else:
            transaction = _create_wallet_transaction(payload)

        insert_operation(transaction)
        response = _addtitional_transactions_informations(transaction, payload)
        return tastypie.create_response(request, response)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)

def _credit_or_debit_entity(transaction):
    if transaction.transaction_type == 'DEBIT_COMPTE_ENTITE':
        _credit_entity(transaction.agent, transaction.amount)
    else:
        _debit_entity(transaction.agent, transaction.paid_amount, transaction.grille.fee)

@agent_code_required
def _create_agent_transaction(payload, token):
    agent = _get_agent_info(payload)
    _check_agent_balance(agent, payload)
    transaction = create_transaction(payload, agent)
    _credit_or_debit_entity(transaction)
    return transaction


def _create_wallet_transaction(payload):
    customer = _get_customer_info(payload)
    _check_customer_balance(customer, payload)
    transaction = create_transaction(payload, customer)
    return transaction


def search(tastypie, payload, request):
    try:
        _validate_search_transaction_by_code_payload(payload.copy())
        _get_agent_info(payload)
        transaction = search_transaction(payload)
        payload = _dump_transaction_payload(transaction)
        payload.get('source_content_object').update(
            _addtitional_customer_informations(payload.get('source_content_object')))
        payload.get('destination_content_object').update(
            _addtitional_customer_informations(payload.get('destination_content_object')))
        return tastypie.create_response(request, payload)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err.messages), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


def pay(tastypie, payload, request):
    try:
        _validate_transaction_payload(payload.copy())
        agent = _get_agent_info(payload)
        transaction = pay_transaction(payload, agent)
        _credit_entity(agent, Decimal(payload.get('paid_amount')))
        insert_operation(transaction)
        return tastypie.create_response(request, {'reponse_code': '000'})
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err.messages), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)
