
from decimal import Decimal
import json
from core.errors import CoreException
from marshmallow import ValidationError
from core.utils.validator import Cash2CashValidator, SearchTransactionCodeValidator,\
    RetraitCashValidator, FeeValidator, CardActivationValidator, SenderCustomerValidator
from shared.models.price import TransactionType
from tastypie.http import HttpUnauthorized, HttpForbidden
from entity.repository.agent_repository import AgentRepository
from kyc.repository.kyc_repository import CustomerRepository
from entity.domain.entity_domain import check_entity_balance, get_entity_balance_by_agent
from transaction.domain.transaction_domain import debit_entity_account, create_transaction, \
    insert_operation, search_transaction, pay_transaction,\
    credit_entity_account, calculate_transaction_fee


def _validate_transaction_payload(payload):
    transaction_type = payload.pop('type')
    try:
        if transaction_type == TransactionType.CASH_TO_CASH.value:
            Cash2CashValidator().load(payload)
        if transaction_type == TransactionType.RETRAIT_CASH.value:
            RetraitCashValidator().load(payload)
        if transaction_type == TransactionType.ACTIVATION_CARTE.value:
            CardActivationValidator().load(payload)
        if transaction_type == TransactionType.CREATION_WALLET.value:
            SenderCustomerValidator().load(payload)
    except ValidationError as err:
        raise ValidationError(str(err))


def _dump_transaction_payload(transaction):
    try:
        transaction_type = transaction.grille.corridor.transaction_type
        if transaction_type == TransactionType.CASH_TO_CASH.value:
            return json.loads(Cash2CashValidator().dumps(transaction))
    except ValidationError as err:
        raise ValidationError(str(err))


def _validate_search_transaction_by_code_payload(payload):
    try:
        SearchTransactionCodeValidator().load(payload)
    except ValidationError as err:
        raise ValidationError(str(err))

def _get_agent_info(payload):
    return AgentRepository.fetch_by_code(payload.get('agent').get('code'))


def _check_agent_balance(agent, payload):
    if not check_entity_balance(agent, payload.get('paid_amount')):
        raise CoreException('agent does not have enough balance', 'agent does not have enough balance')


def _debit_entity(agent, amount, fee=0):
    last_balance = get_entity_balance_by_agent(agent)
    print('last_balance', last_balance)
    debit_entity_account(agent, last_balance, amount)


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
        agent = _get_agent_info(payload)
        _check_agent_balance(agent, payload)
        transaction = create_transaction(payload, agent)
        _debit_entity(agent, payload.get(
            'paid_amount'), transaction.grille.fee)
        insert_operation(transaction)
        response = _addtitional_transactions_informations(transaction, payload)
        return tastypie.create_response(request, response)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


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
