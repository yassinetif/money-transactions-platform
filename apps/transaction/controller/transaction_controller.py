
import json
from apps.core.errors import CoreException, CustomerException
from apps.core.utils.http import get_request_token
from apps.core.utils.string import format_decimal_with_two_digits_after_comma, convert_sharing_calculation_expression_to_json, convert_snake_to_camel_case
from marshmallow import ValidationError
from importlib import import_module
from apps.core.utils.validator import SearchTransactionCodeValidator, FeeValidator
from tastypie.http import HttpUnauthorized, HttpForbidden
from apps.entity.repository.agent_repository import AgentRepository
from apps.entity.repository.entity_repository import EntityRepository
from apps.kyc.repository.kyc_repository import CustomerRepository
from apps.kyc.domain.customer_domain import check_customer_balance, get_customer_balance, debit_customer_account
from apps.entity.domain.entity_domain import check_entity_balance, get_entity_balance_by_agent
from apps.transaction.domain.transaction_domain import debit_entity_account, create_transaction, \
    insert_operation, search_transaction, pay_transaction,\
    credit_entity_account, calculate_transaction_paid_amount_and_fee,\
    currency_change, get_fee_calculation_payload
from apps.transaction.decorator.transaction_decorator import agent_code_required, customer_code_required
from apps.transaction.repository.transaction_repository import TransactionRepository
from apps.shared.models.price import AGENT_TRANSACTIONS
from apps.shared.repository.shared_repository import SharedRepository
from numexpr import evaluate as ev
from decimal import Decimal

def _get_validator_class(transaction_type):
    validator = convert_snake_to_camel_case(transaction_type)
    module = import_module('apps.core.utils.validator')
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


def _debit_entity(transaction):
    last_balance = get_entity_balance_by_agent(transaction.agent)
    debit_entity_account(transaction.agent, last_balance, transaction.paid_amount)


def _debit_customer(customer, amount, fee=0):
    last_balance = get_customer_balance(customer)
    debit_customer_account(customer, last_balance, amount)


def _credit_entity(transaction):
    last_balance = get_entity_balance_by_agent(transaction.agent)
    changed_amount = currency_change(transaction.grille.corridor.currency,
                                     transaction.destination_country.currency, transaction.amount)
    credit_entity_account(transaction.agent, last_balance, changed_amount)


def _addtitional_transactions_informations(transaction, payload):
    info = {'transaction_number': transaction.number, 'receipt_code': transaction.code}
    payload.update(info)
    payload.update({'response_code': '000', 'date': transaction.created})
    payload.update({'destination_currency': transaction.destination_country.currency.iso})
    payload.update({'source_currency': transaction.source_country.currency.iso})
    payload.update({'operation_amount': transaction.operation_amount})
    payload.update({'source_revenu': transaction.source_revenu.libelle})
    payload.update({'motif_envoi': transaction.motif_envoi.libelle})
    payload.update({'parity': SharedRepository.fetch_change_parity_value(transaction.source_country.currency,
                                                                         transaction.destination_country.currency)})

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
        total_fee, total_amount = calculate_transaction_paid_amount_and_fee(payload)
        response = {'response_code': '000', 'fee': format_decimal_with_two_digits_after_comma(total_fee), 'total_amount': format_decimal_with_two_digits_after_comma(total_amount)}
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
        else:
            transaction = _create_wallet_transaction(payload, token)

        insert_operation(transaction)
        _response = _addtitional_transactions_informations(transaction, payload)
        response = _add_agent_informations(transaction, _response)
        return tastypie.create_response(request, response)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)

def _credit_or_debit_entity(transaction):
    if transaction.transaction_type == 'DEBIT_COMPTE_ENTITE':
        _credit_entity(transaction)
    else:
        _debit_entity(transaction)

@agent_code_required
def _create_agent_transaction(payload, token):
    agent = _get_agent_info(payload)
    payload.update({'source_country': agent.entity.country.iso.code})
    fee_calculation_payload = get_fee_calculation_payload(payload)
    fee, paid_amount = calculate_transaction_paid_amount_and_fee(fee_calculation_payload)

    payload.update({'paid_amount': format_decimal_with_two_digits_after_comma(paid_amount)})
    payload.update({'fee': format_decimal_with_two_digits_after_comma(fee)})
    _check_agent_balance(agent, payload)
    transaction = create_transaction(payload, agent)
    _credit_or_debit_entity(transaction)
    _revenu_sharing(transaction)
    return transaction


def _add_agent_informations(transaction, payload):
    transaction_type = payload.get('type')
    if transaction_type in AGENT_TRANSACTIONS:
        agent_informations = AgentRepository.to_json(payload.get('agent').get('code'))
        payload.update({'agent': agent_informations})
        payload.update({'payer': {'brand_name':'Monamon','logo':''}})
    return payload

@customer_code_required
def _create_wallet_transaction(payload, token):
    payload.update({'source_content_object': {'phone_number': payload.get('code')}})
    del payload['code']
    customer = _get_customer_info(payload)
    payload.update({'source_country': customer.country.iso.code})
    fee_calculation_payload = get_fee_calculation_payload(payload)
    paid_amount = calculate_transaction_paid_amount_and_fee(fee_calculation_payload)[1]
    payload.update({'paid_amount': paid_amount})
    _check_customer_balance(customer, payload)
    transaction = create_transaction(payload, customer)
    return transaction


@agent_code_required
def search_transaction_code(payload, token):
    agent = _get_agent_info(payload)
    transaction = search_transaction(payload)
    payload = _dump_transaction_payload(transaction)
    payload.get('source_content_object').update(
        _addtitional_customer_informations(payload.get('source_content_object')))
    payload.get('destination_content_object').update(
        _addtitional_customer_informations(payload.get('destination_content_object')))
    amount = transaction.amount
    converted_amount = currency_change(transaction.agent.entity.country.currency.iso, agent.entity.country.currency.iso, amount)
    payload.update({'amount': format_decimal_with_two_digits_after_comma(converted_amount)})
    return payload


def search(tastypie, payload, request):
    try:
        _validate_search_transaction_by_code_payload(payload.copy())
        token = get_request_token(request)
        result = search_transaction_code(payload, token)
        return tastypie.create_response(request, result)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err.messages), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


def pay(tastypie, payload, request):
    try:
        _validate_transaction_payload(payload.copy())
        token = get_request_token(request)
        _pay_transaction(payload, token)
        return tastypie.create_response(request, {'response_code': '000'})
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err.messages), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)

@agent_code_required
def _pay_transaction(payload, token):
    agent = _get_agent_info(payload)
    transaction = pay_transaction(payload, agent)
    _credit_entity(transaction)
    insert_operation(transaction)


def _revenu_sharing(transaction):
    expression = SharedRepository.fetch_sharing_calculation_expression(transaction)
    json_expression = convert_sharing_calculation_expression_to_json(expression)
    fee_value = _get_fee_value(transaction, json_expression.pop('fee'))
    json_expression = _calculate_real_revenue_of_each_participant_of_transaction(json_expression, fee_value)
    _dispatch_revenu_in_accounts(transaction, json_expression)

    return json_expression

def _calculate_real_revenue_of_each_participant_of_transaction(json_expression, fee_value):
    for e, val in json_expression.items():
        json_expression.update({e: '{0}{1}'.format(val[:1], ev('{0}*{1}'.format(val[1:], fee_value)))})
    return json_expression

def _get_fee_value(transaction, fee_expression):
    fee_expression = fee_expression.replace('FEE', str(transaction.grille.fee))
    return str(float(ev(fee_expression)))

def _dispatch_revenu_in_accounts(transaction, json_expression):
    if transaction.transaction_type in AGENT_TRANSACTIONS:
        for e, value in json_expression.items():
            entity = EntityRepository.fetch_entity_by_type_and_hierarchy(transaction.agent.entity, e)
            amount = currency_change(transaction.grille.corridor.currency,
                                     entity.country.currency, Decimal(value))
            TransactionRepository.save_entity_commission(transaction, entity, amount)
