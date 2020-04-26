from decimal import Decimal
from shared.models.account import Account, AccountType
from core.errors import CoreException


def check_entity_balance(agent, amount):
    last_balance = get_entity_balance_by_agent(agent)
    return last_balance - Decimal(amount) >= 0


def get_entity_balance_by_agent(agent):
    return agent.entity.accounts.last().balance


def get_entity_balance(entity):
    return entity.accounts.last().balance


def credit_entity(entity, last_balance, amount):
    if amount < 0:
        raise CoreException('unable to credit entity', 'transaction failed')

    Account.objects.create(content_object=entity,
                           category=AccountType.PRINCIPAL, balance=last_balance+Decimal(amount))


def debit_entity(entity, last_balance, amount):
    if amount < 0:
        raise CoreException('unable to debit entity', 'transaction failed')
    Account.objects.create(content_object=entity,
                           category=AccountType.PRINCIPAL, balance=last_balance-Decimal(amount))
