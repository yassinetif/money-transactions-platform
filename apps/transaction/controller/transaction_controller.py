
from decimal import Decimal
import logging
from core.errors import CoreException
from marshmallow import ValidationError
from transaction.validator import Cash2CashValidator, SearchTransactionCodeValidator
from shared.models import TransactionType
from transaction.models import Transaction
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpAccepted
from entity.repository.agent_repository import AgentRepository
from shared.repository.shared_repository import SharedRepository
from entity.domain.entity_domain import check_entity_balance, get_entity_balance_by_agent
from transaction.domain.transaction_domain import get_source_and_destination_of_transaction,\
    debit_entity_account, create_transaction, insert_operation, search_transaction
logger = logging.getLogger(__name__)


def _validate_transaction_payload(payload: dict):
    transaction_type = payload.pop('type')
    if transaction_type == TransactionType.CASH_TO_CASH.value:
        Cash2CashValidator().load(payload)


def _validate_search_transaction_by_code_payload(payload: dict):
    SearchTransactionCodeValidator().load(payload)


def _get_agent_info(payload: dict):
    return AgentRepository.fetch_by_code(payload.get('agent').get('code'))


def _check_agent_balance(agent, payload: dict) -> bool:
    if not check_entity_balance(agent, payload.get('amount')):
        raise CoreException('transaction can not continue',
                            'agent does not have enough balance')


def _debit_entity(agent, amount: Decimal):
    last_balance = get_entity_balance_by_agent(agent)
    debit_entity_account(agent, last_balance, amount)


def create(tastypie, payload, request):

    try:
        _validate_transaction_payload(payload.copy())
        agent = _get_agent_info(payload)
        _check_agent_balance(agent, payload)

        transaction = create_transaction(payload, agent)
        _debit_entity(agent, payload.get('amount'))

        insert_operation(transaction)

        return tastypie.create_response(request, payload)
    except ValidationError as err:
        return tastypie.create_response(request, {'reason': err.messages}, HttpUnauthorized)
    except CoreException as err:
        logging.error(err, err.errors)
        return tastypie.create_response(request, {'reason': err.errors}, HttpForbidden)


def search(tastypie, payload, request):

    try:
        _validate_search_transaction_by_code_payload(payload.copy())
        _get_agent_info(payload)

        transaction = search_transaction(payload)

        return tastypie.create_response(request, payload)
    except ValidationError as err:
        return tastypie.create_response(request, {'reason': err.messages}, HttpUnauthorized)
    except CoreException as err:
        logging.error(err, err.errors)
        return tastypie.create_response(request, {'reason': err.errors}, HttpForbidden)
