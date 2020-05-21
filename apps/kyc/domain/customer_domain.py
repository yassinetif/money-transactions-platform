from decimal import Decimal
from apps.shared.models.account import Account, AccountType
from apps.core.errors import CustomerException


def check_customer_balance(customer, amount):
    last_balance = get_customer_balance(customer)
    return last_balance - Decimal(amount) >= 0

def get_customer_balance(customer):
    return customer.accounts.last().balance


def credit_customer_account(customer, last_balance, amount):
    if Decimal(amount) < 0:
        raise CustomerException('unable to credit customer Wallet', 'transaction failed')

    Account.objects.create(content_object=customer,
                           category=AccountType.PRINCIPAL.value, balance=last_balance+Decimal(amount))


def debit_customer_account(customer, last_balance, amount):
    if Decimal(amount) < 0:
        raise CustomerException('unable to debit customer Wallet', 'transaction failed')
    Account.objects.create(content_object=customer,
                           category=AccountType.PRINCIPAL.value, balance=last_balance-Decimal(amount))
