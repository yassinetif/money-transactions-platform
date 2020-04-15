from decimal import Decimal
from entity.models import Agent, Entity
from shared.models import Account, AccountType


def check_entity_balance(agent: Agent, amount: Decimal) -> Decimal:
    last_balance = agent.entity.accounts.last().balance
    return last_balance - Decimal(amount) >= 0


def get_entity_balance_by_agent(agent: Agent) -> Decimal:
    return agent.entity.accounts.last().balance


def get_entity_balance(entity: Entity) -> Decimal:
    return entity.accounts.last().balance


def credit_entity(entity: Entity, last_balance: Decimal, amount: Decimal):
    Account.objects.create(content_object=entity,
                           category=AccountType.PRINCIPAL, balance=last_balance+Decimal(amount))


def debit_entity(entity: Entity, last_balance: Decimal, amount: Decimal):
    Account.objects.create(content_object=entity,
                           category=AccountType.PRINCIPAL, balance=last_balance-Decimal(amount))
