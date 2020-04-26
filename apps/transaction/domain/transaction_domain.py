from core.errors import CoreException
from shared.repository.shared_repository import SharedRepository
from kyc.repository.kyc_repository import CustomerRepository
from entity.domain.entity_domain import debit_entity, credit_entity
from shared.models.price import TransactionType
from ..models import Transaction, Operation, TransactionStatus, TransactionCodePrefix
from transaction.repository.transaction_repository import TransactionRepository
from core.utils.string import random_code, convert_enum_to_tuple
from importlib import import_module


def get_grille_tarifaire(payload):
    amount = payload.get('amount')
    source_country = payload.get('source_country')
    destination_country = payload.get('destination_country')
    transaction_type = payload.get('type')
    corridor = SharedRepository.fetch_corridor_by_source_and_destination(
        transaction_type, source_country, destination_country)
    grille = SharedRepository.fetch_grille_by_corridor(corridor, amount)
    return grille


def get_source_and_destination_of_transaction(payload):
    transaction_type = payload.get('type')
    if transaction_type == TransactionType.CASH_TO_CASH.value:
        source = CustomerRepository.fetch_or_create_customer(
            payload.get('source_content_object'))
        destination = CustomerRepository.fetch_or_create_customer(
            payload.get('destination_content_object'))
    return source, destination


def debit_entity_account(agent, last_balance, amount):
    debit_entity(agent.entity, last_balance, amount)


def credit_entity_account(agent, last_balance, amount):
    credit_entity(agent.entity, last_balance, amount)


def create_transaction(payload, agent):
    source, destination = get_source_and_destination_of_transaction(
        payload.copy())
    transaction = Transaction()
    transaction.transaction_type = TransactionType.CASH_TO_CASH.value
    transaction.agent = agent
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = source
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.source_country = SharedRepository.fetch_country_by_iso(
        payload.get('source_country'))
    transaction.destination_country = SharedRepository.fetch_country_by_iso(
        payload.get('destination_country'))
    transaction.save()

    return transaction


def get_partner_module_name(code):
    for _prefix in convert_enum_to_tuple(TransactionCodePrefix):
        if code.startswith(_prefix):
            return 'transaction.domain.{0}_domain'.format(TransactionCodePrefix(_prefix).name.lower())
    return None


def download_transaction_from_partner(payload, partner_module):
    module = import_module(partner_module)
    transaction = module.search_transaction(payload)
    return transaction


def search_transaction(payload):
    code = payload.get('code')
    partner_module = get_partner_module_name(code)
    if partner_module:
        download_transaction_from_partner(payload, partner_module)

    return TransactionRepository.fetch_unpaid_transaction_by_code(code)


def pay_transaction(payload, agent):
    transaction = search_transaction(payload)
    _can_agent_pay_transaction(transaction, agent)

    parent = transaction
    parent.status = TransactionStatus.SUCCESS.value
    parent.save()

    transaction.pk = None
    transaction.number = random_code(10)
    transaction.code = random_code(8)
    transaction.status = TransactionStatus.SUCCESS.value
    transaction.parent_transaction_number = parent.number
    transaction.transaction_type = TransactionType.RETRAIT_CASH.value
    transaction.agent = agent
    transaction.save()
    return transaction


def insert_operation(transaction):
    operation = Operation()
    operation.comment = _get_operation_comment(transaction)
    operation.balance_after_operation = transaction.agent\
        .entity.accounts.last()
    operation.transaction = transaction
    operation.save()


def _get_operation_comment(transaction):
    comment = ''
    if transaction.transaction_type == TransactionType.CASH_TO_CASH.value:
        comment = 'Débit de {0} : transaction {1}'.format(transaction.paid_amount, transaction.number)
    elif transaction.transaction_type == TransactionType.RETRAIT_CASH.value:
        comment = 'Crédit de {0} : transaction {1}'.format(transaction.amount, transaction.number)
    return comment

    # TODO : def share_transaction_revenu(transaction: Transaction):
    # TODO calculation_expression = transaction.corr


def _can_agent_pay_transaction(transaction, agent):
    if transaction.agent == agent:
        raise CoreException('agent can not be affected to this operation', '')
    else:
        return True
