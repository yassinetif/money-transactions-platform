from shared.models import Grille, Corridor, Account
from shared.repository.shared_repository import SharedRepository
from kyc.repository.kyc_repository import CustomerRepository
from entity.domain.entity_domain import debit_entity, get_entity_balance, credit_entity
from shared.models import TransactionType
from ..models import Transaction, Operation
from transaction.repository.transaction_repository import TransactionRepository
from decimal import Decimal

def get_grille_tarifaire(payload: dict) -> Grille:
    amount = payload.get('amount')
    source_country = payload.get('source_country')
    destination_country = payload.get('destination_country')
    transaction_type = payload.get('type')
    corridor = SharedRepository.fetch_corridor_by_source_and_destination(
        transaction_type, source_country, destination_country)
    grille = SharedRepository.fetch_grille_by_corridor(corridor, amount)
    return grille


def get_source_and_destination_of_transaction(payload: dict):
    transaction_type = payload.get('type')
    if transaction_type == TransactionType.CASH_TO_CASH.value:
        source = _get_or_create_customer(payload.get('sender'))
        destination = _get_or_create_customer(payload.get('receiver'))
    return source, destination


def _get_or_create_customer(payload: dict):
    customer = CustomerRepository.fetch_or_create_customer(payload)
    return customer


def debit_entity_account(agent, last_balance: Decimal, amount: Decimal):
    debit_entity(agent.entity, last_balance, amount)


def create_transaction(payload: dict, agent) -> Transaction:
    source, destination = get_source_and_destination_of_transaction(
        payload.copy())
    transaction = Transaction()
    transaction.agent = agent
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = source
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.save()

    return transaction

def search_transaction(payload:dict) -> dict :
    transaction = TransactionRepository.fetch_transaction_by_code(payload.get('code'))



def insert_operation(transaction: Transaction):
    operation = Operation()
    operation.comment = transaction.grille.corridor.transaction_type
    operation.balance_after_operation = transaction.agent\
        .entity.accounts.last()
    operation.transaction = transaction
    operation.save()


# def share_transaction_revenu(transaction: Transaction):
#    calculation_expression = transaction.corr
