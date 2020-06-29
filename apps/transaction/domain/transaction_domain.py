from apps.core.errors import CoreException
from apps.shared.repository.shared_repository import SharedRepository
from apps.kyc.repository.kyc_repository import CustomerRepository
from apps.entity.repository.entity_repository import EntityRepository
from apps.entity.repository.agent_repository import AgentRepository
from apps.entity.domain.entity_domain import debit_entity, credit_entity, get_entity_balance
from apps.kyc.domain.customer_domain import credit_customer_account, get_customer_balance, debit_customer_account
from apps.shared.models.price import TransactionType
from apps.transaction.models import Transaction, Operation, TransactionStatus, TransactionCodePrefix
from apps.transaction.repository.transaction_repository import TransactionRepository
from apps.core.utils.string import random_code, convert_enum_to_tuple
from apps.core.utils.http import post_simple_json_request
from importlib import import_module
from decimal import Decimal

CURRENT_MODULE = 'apps.transaction.domain.transaction_domain'

def get_source_and_destination_currencies(source_country, destination_country):
    source_currency_iso = SharedRepository.fetch_currency_by_country_iso(source_country)
    destination_currency_iso = SharedRepository.fetch_currency_by_country_iso(destination_country)
    return source_currency_iso, destination_currency_iso


def get_grille_tarifaire(payload):
    amount = payload.get('amount')
    source_country = payload.get('source_country')
    destination_country = payload.get('destination_country')
    transaction_type = payload.get('type')
    corridor = SharedRepository.fetch_corridor_by_source_and_destination(transaction_type, source_country, destination_country)
    source_currency_iso, _ = get_source_and_destination_currencies(source_country, destination_country)
    converted_amount = currency_change(source_currency_iso, corridor.currency.iso, Decimal(amount))
    grille = SharedRepository.fetch_grille_by_corridor(corridor, converted_amount)
    return grille


def calculate_transaction_fee(payload):
    grille = get_grille_tarifaire(payload)
    amount = Decimal(payload.get('amount'))
    source_currency_iso, _ = get_source_and_destination_currencies(payload.get('source_country'), payload.get('destination_country'))
    converted_amount = currency_change(source_currency_iso, grille.corridor.currency.iso, amount)
    fee = SharedRepository.get_fee_by_grille(grille, converted_amount)
    converted_fee = currency_change(grille.corridor.currency.iso, source_currency_iso, fee)
    return converted_fee


def calculate_transaction_paid_amount_and_fee(payload):
    print('je suis ici')
    fee = calculate_transaction_fee(payload)
    print('je suis ici aussi')
    total = fee + Decimal(payload.get('amount'))
    print('je suis ici ')
    return fee, total


def currency_change(source_currency, destination_currency, amount):
    parity = SharedRepository.fetch_change_parity_value(source_currency, destination_currency)
    return amount * parity


def get_fee_calculation_payload(payload):
    module = import_module(CURRENT_MODULE)
    method = getattr(module, 'get_{0}_fee_payload'.format(payload.get('type').lower()))
    return method(payload)

def get_debit_compte_entite_fee_payload(payload):
    data = get_credit_compte_entite_fee_payload(payload)
    return data

def get_wallet_to_wallet_fee_payload(payload):
    data = {}
    destination_country = CustomerRepository.fetch_customer_by_phone_number(payload.get('destination_content_object').get('phone_number')).country.iso.code
    data.update({'source_country': payload.get('source_country')})
    data.update({'type': payload.get('type')})
    data.update({'destination_country': destination_country})
    data.update({'amount': payload.get('amount')})
    return data

def get_credit_compte_entite_fee_payload(payload):
    data = {}
    destination_country = EntityRepository.fetch_by_account_number(payload.get('account_number')).country.iso.code
    data.update({'source_country': payload.get('source_country')})
    data.update({'type': payload.get('type')})
    data.update({'destination_country': destination_country})
    data.update({'amount': payload.get('amount')})
    return data

def get_activation_carte_fee_payload(payload):
    data = {}
    data.update({'source_country': payload.get('customer').get('country')})
    data.update({'type': payload.get('type')})
    data.update({'destination_country': payload.get('customer').get('country')})
    data.update({'amount': payload.get('amount')})
    return data

def get_cash_to_cash_fee_payload(payload):
    data = {}
    data.update({'source_country': payload.get('source_country')})
    data.update({'type': payload.get('type')})
    data.update({'destination_country': payload.get('destination_country')})
    data.update({'amount': payload.get('amount')})
    return data


def get_cash_to_bank_account_fee_payload(payload):
    data = {}
    data.update({'source_country': payload.get('source_country')})
    data.update({'type': payload.get('type')})
    data.update({'destination_country': payload.get('destination_country')})
    data.update({'amount': payload.get('amount')})
    return data

def get_cash_to_wallet_fee_payload(payload):
    data = {}
    data.update({'source_country': payload.get('source_country')})
    data.update({'type': payload.get('type')})
    data.update({'destination_country': CustomerRepository.fetch_customer_by_phone_number(payload.get('destination_content_object').get('phone_number')).country.iso.code})
    data.update({'amount': payload.get('amount')})
    return data

def get_wallet_to_cash_fee_payload(payload):
    data = {}
    data.update({'source_country': payload.get('source_country')})
    data.update({'type': payload.get('type')})
    data.update({'destination_country': payload.get('destination_content_object').get('country')})
    data.update({'amount': payload.get('amount')})
    return data


def get_source_and_destination_of_transaction(payload):
    module = import_module(CURRENT_MODULE)
    method = getattr(module, 'get_source_and_destination_of_{0}'.format(payload.get('type').lower()))
    return method(payload)


def get_source_and_destination_of_cash_to_cash(payload):
    source = CustomerRepository.fetch_or_create_customer(payload.get('source_content_object'))
    destination = CustomerRepository.fetch_or_create_customer(payload.get('destination_content_object'))
    return source, destination

def get_source_and_destination_of_activation_carte(payload):
    source = CustomerRepository.fetch_or_create_customer(payload.get('customer'), True)
    destination = EntityRepository.fetch_by_agent_code(payload.get('agent').get('code'))
    return source, destination

def get_source_and_destination_of_credit_compte_entite(payload):
    source = None
    destination = EntityRepository.fetch_by_account_number(payload.get('account_number'))
    return source, destination


def get_source_and_destination_of_debit_compte_entite(payload):
    return get_source_and_destination_of_credit_compte_entite(payload)


def get_source_and_destination_of_cash_to_wallet(payload):
    source = CustomerRepository.fetch_or_create_customer(payload.get('source_content_object'))
    destination = CustomerRepository.fetch_customer_by_phone_number(payload.get('destination_content_object').get('phone_number'))
    return source, destination


def get_source_and_destination_of_wallet_to_wallet(payload):
    source = CustomerRepository.fetch_customer_by_phone_number(payload.get('destination_content_object').get('phone_number'))
    destination = CustomerRepository.fetch_customer_by_phone_number(payload.get('destination_content_object').get('phone_number'))
    return source, destination

def get_source_and_destination_of_wallet_to_cash(payload):
    source = None
    destination = CustomerRepository.fetch_or_create_customer(payload.get('destination_content_object'))
    return source, destination


def get_source_and_destination_of_cash_to_bank_account(payload):
    source = CustomerRepository.fetch_or_create_customer(payload.get('source_content_object'))
    destination = CustomerRepository.fetch_or_create_customer(payload.get('destination_content_object'))
    return source, destination


def create_relation_between(source, destination):
    if destination not in source.relations.all():
        source.relations.add(destination)
        source.save()


def debit_entity_account(agent, last_balance, amount):
    debit_entity(agent.entity, last_balance, amount)

def credit_entity_account(agent, last_balance, amount):
    credit_entity(agent.entity, last_balance, amount)

def create_transaction(payload, executer):
    transaction_type = payload.get('type')
    _ = transaction_type.lower()
    module = import_module(CURRENT_MODULE)
    method = getattr(module, '_create_{0}_transaction'.format(_))
    return method(payload, executer)


def _create_cash_to_cash_transaction(payload, agent):
    source, destination = get_source_and_destination_of_transaction(
        payload.copy())
    transaction = Transaction()
    transaction.transaction_type = TransactionType.CASH_TO_CASH.value
    transaction.agent = agent
    transaction.number = random_code(10)
    transaction.code = random_code(9)
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = source
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.source_country = SharedRepository.fetch_country_by_iso(
        payload.get('source_country'))
    transaction.destination_country = SharedRepository.fetch_country_by_iso(
        payload.get('destination_country'))
    transaction.source_revenu = SharedRepository.fetch_source_revenu_libelle_by_code(payload.get('source_revenu'))
    transaction.motif_envoi = SharedRepository.fetch_motif_envoi_libelle_by_code(payload.get('motif_envoi'))
    transaction.save()
    create_relation_between(source, destination)
    return transaction


def _create_cash_to_bank_account_transaction(payload, agent):
    source, destination = get_source_and_destination_of_transaction(
        payload.copy())
    transaction = Transaction()
    transaction.transaction_type = TransactionType.CASH_TO_CASH.value
    transaction.agent = agent
    transaction.number = random_code(10)
    transaction.code = random_code(9)
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = source
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.source_country = SharedRepository.fetch_country_by_iso(
        payload.get('source_country'))
    transaction.destination_country = SharedRepository.fetch_country_by_iso(
        payload.get('destination_country'))
    transaction.other_informations = 'BANQUE : {}, RIB : {}'.format(payload.get('bank_name'), payload.get('rib'))
    transaction.source_revenu = SharedRepository.fetch_source_revenu_libelle_by_code(payload.get('source_revenu'))
    transaction.motif_envoi = SharedRepository.fetch_motif_envoi_libelle_by_code(payload.get('motif_envoi'))
    transaction.save()
    create_relation_between(source, destination)
    return transaction

def _create_activation_carte_transaction(payload, agent):

    payload.update({'source_country': payload.get('customer').get('country'),
                    'destination_country': agent.entity.country.iso})
    source, destination = get_source_and_destination_of_transaction(
        payload.copy())
    transaction = Transaction()
    transaction.transaction_type = TransactionType.ACTIVATION_CARTE.value
    transaction.agent = agent
    transaction.number = random_code(10)
    transaction.code = random_code(9)
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = source
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.status = TransactionStatus.SUCCESS.value
    transaction.source_country = agent.entity.country
    transaction.destination_country = SharedRepository.fetch_country_by_iso(
        payload.get('customer').get('country'))
    transaction.save()
    return transaction


def _create_credit_compte_entite_transaction(payload, agent):
    _, destination = get_source_and_destination_of_transaction(
        payload.copy())
    _can_agent_execute_transaction(agent.entity, destination)
    payload.update({'source_country': agent.entity.country.iso,
                    'destination_country': destination.country.iso})

    operation_amount = currency_change(agent.entity.country.currency.iso, destination.country.currency.iso, Decimal(payload.get('amount')))

    transaction = Transaction()
    transaction.transaction_type = TransactionType.CREDIT_COMPTE_ENTITE.value
    transaction.agent = agent
    transaction.number = random_code(10)
    transaction.code = random_code(9)
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = agent.entity
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.source_country = agent.entity.country
    transaction.destination_country = destination.country
    transaction.status = TransactionStatus.SUCCESS.value
    transaction.paid_amount_in_destination_currency = operation_amount
    transaction.save()

    credit_entity(destination, get_entity_balance(destination), operation_amount)
    return transaction


def _create_debit_compte_entite_transaction(payload, agent):
    _, destination = get_source_and_destination_of_transaction(
        payload.copy())
    _can_agent_execute_transaction(agent.entity, destination)
    payload.update({'source_country': agent.entity.country.iso,
                    'destination_country': destination.country.iso})

    operation_amount = currency_change(agent.entity.country.currency.iso, destination.country.currency.iso, Decimal(payload.get('amount')))

    transaction = Transaction()
    transaction.transaction_type = TransactionType.DEBIT_COMPTE_ENTITE.value
    transaction.agent = agent
    transaction.number = random_code(10)
    transaction.code = random_code(9)
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = agent.entity
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.source_country = agent.entity.country
    transaction.destination_country = destination.country
    transaction.status = TransactionStatus.SUCCESS.value
    transaction.paid_amount_in_destination_currency = operation_amount
    transaction.save()

    debit_entity(destination, get_entity_balance(destination), payload.get('amount'))
    return transaction

def _create_cash_to_wallet_transaction(payload, agent):

    source, destination = get_source_and_destination_of_transaction(
        payload.copy())
    payload.update({'source_country': agent.entity.country.iso,
                    'destination_country': destination.country.iso})

    operation_amount = currency_change(agent.entity.country.currency.iso, destination.country.currency.iso, Decimal(payload.get('amount')))

    transaction = Transaction()
    transaction.transaction_type = TransactionType.CASH_TO_WALLET.value
    transaction.agent = agent
    transaction.number = random_code(10)
    transaction.code = random_code(9)
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = source
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.source_country = agent.entity.country
    transaction.destination_country = destination.country
    transaction.status = TransactionStatus.SUCCESS.value
    transaction.paid_amount_in_destination_currency = operation_amount
    transaction.save()

    credit_customer_account(destination, get_customer_balance(destination), operation_amount)
    return transaction

def _create_wallet_to_cash_transaction(payload, customer):

    _, destination = get_source_and_destination_of_transaction(
        payload.copy())
    payload.update({'source_country': customer.country.iso,
                    'destination_country': destination.country.iso})
    operation_amount = currency_change(customer.country.currency.iso, destination.country.currency.iso, Decimal(payload.get('amount')))

    transaction = Transaction()
    transaction.transaction_type = TransactionType.WALLET_TO_CASH.value
    transaction.number = random_code(10)
    transaction.code = random_code(9)
    transaction.agent = AgentRepository.fetch_by_username('AGENT_WALLET')
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = customer
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.source_country = customer.country
    transaction.destination_country = destination.country
    transaction.paid_amount_in_destination_currency = operation_amount
    transaction.save()

    debit_customer_account(customer, get_customer_balance(customer), payload.get('paid_amount'))
    create_relation_between(customer, destination)
    return transaction

def _create_wallet_to_wallet_transaction(payload, customer):

    _, destination = get_source_and_destination_of_transaction(
        payload.copy())
    payload.update({'source_country': customer.country.iso,
                    'destination_country': destination.country.iso})
    operation_amount = currency_change(customer.country.currency.iso, destination.country.currency.iso, Decimal(payload.get('amount')))

    transaction = Transaction()
    transaction.transaction_type = TransactionType.WALLET_TO_WALLET.value
    transaction.number = random_code(10)
    transaction.code = random_code(9)
    transaction.agent = AgentRepository.fetch_by_username('AGENT_WALLET')
    transaction.amount = payload.get('amount')
    transaction.paid_amount = payload.get('paid_amount')
    transaction.source_content_object = customer
    transaction.destination_content_object = destination
    transaction.grille = get_grille_tarifaire(payload)
    transaction.source_country = customer.country
    transaction.destination_country = destination.country
    transaction.paid_amount_in_destination_currency = operation_amount

    transaction.save()

    debit_customer_account(customer, get_customer_balance(customer), payload.get('paid_amount'))
    credit_customer_account(destination, get_customer_balance(destination), operation_amount)
    create_relation_between(customer, destination)
    return transaction


def get_partner_module_name(code):
    for _prefix in convert_enum_to_tuple(TransactionCodePrefix):
        if code.startswith(_prefix):
            return 'transaction.domain.{0}_domain'.format(TransactionCodePrefix(_prefix).name.lower())
    return None


def download_transaction_from_partner(payload, partner_module):
    module = import_module(partner_module)
    transaction_json_data = module.search_transaction(payload)
    return transaction_json_data

def send_partner_downloaded_transaction(payload):
    url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
    response = post_simple_json_request(url, payload)
    return response.json()


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
    transaction.code = random_code(9)
    transaction.amount = currency_change(parent.agent.entity.country.currency.iso, agent.entity.country.currency.iso, parent.amount)
    transaction.paid_amount = currency_change(parent.agent.entity.country.currency.iso, agent.entity.country.currency.iso, parent.paid_amount)
    transaction.status = TransactionStatus.SUCCESS.value
    transaction.parent_transaction_number = parent.number
    transaction.transaction_type = TransactionType.RETRAIT_CASH.value
    transaction.agent = agent
    transaction.save()
    return transaction


def insert_operation(transaction):
    if transaction.transaction_type in [TransactionType.CREDIT_COMPTE_ENTITE.value, TransactionType.CASH_TO_WALLET.value, TransactionType.DEBIT_COMPTE_ENTITE.value]:
        _insert_credit_compte_entite_operation(transaction)

    elif transaction.transaction_type == TransactionType.WALLET_TO_WALLET.value:
        _insert_wallet_to_wallet_operation(transaction)

    elif transaction.transaction_type == TransactionType.WALLET_TO_CASH.value:
        _insert_wallet_to_wallet_operation(transaction, True)

    else:
        operation = Operation()
        operation.comment = _get_operation_comment(transaction)
        operation.balance_after_operation = transaction.agent.entity.accounts.last()
        operation.transaction = transaction
        operation.save()


def _insert_credit_compte_entite_operation(transaction):
    operation_debit = Operation()
    operation_debit.comment = _get_operation_comment(transaction)
    operation_debit.balance_after_operation = transaction.agent.entity.accounts.last()
    operation_debit.transaction = transaction
    operation_debit.save()

    operation_credit = Operation()
    operation_credit.comment = _get_operation_comment(transaction, True)
    operation_credit.balance_after_operation = transaction.destination_content_object.accounts.last()
    operation_credit.transaction = transaction
    operation_credit.save()


def _insert_wallet_to_wallet_operation(transaction, wallet_to_cash=False):
    operation_debit = Operation()
    operation_debit.comment = _get_operation_comment(transaction)
    operation_debit.balance_after_operation = transaction.source_content_object.accounts.last()
    operation_debit.transaction = transaction
    operation_debit.save()

    if wallet_to_cash is False:
        operation_credit = Operation()
        operation_credit.comment = _get_operation_comment(transaction, True)
        operation_credit.balance_after_operation = transaction.destination_content_object.accounts.last()
        operation_credit.transaction = transaction
        operation_credit.save()


def _get_operation_comment(transaction, flag=False):
    module = import_module(CURRENT_MODULE)
    method = getattr(module, '_get_operation_comment_of_{0}'.format(transaction.transaction_type.lower()))
    return method(transaction, flag)

def _get_operation_comment_of_cash_to_cash(transaction, flag=False):
    return 'Débit de {0} : transaction {1}, Transfert d\'argent cash to cash'.format(transaction.paid_amount, transaction.number)

def _get_operation_comment_of_activation_carte(transaction, flag=False):
    return 'Débit de {0} : transaction {1}, Activation d\'une carte Monnamon'.format(transaction.paid_amount, transaction.number)

def _get_operation_comment_of_wallet_to_cash(transaction, flag=False):
    return 'Débit de {0} : transaction {1}, Envoi d\'argent depuis Wallet {2}'.format(transaction.paid_amount, transaction.number, transaction.source_content_object)

def _get_operation_comment_of_retrait_cash(transaction, flag=False):
    return 'Crédit de {0} : transaction {1}, Retrait d\'argent cash to cash'.format(transaction.amount, transaction.number)

def _get_operation_comment_of_credit_compte_entite(transaction, flag=False):
    comment = 'Débit de {0} : transaction {1}, Rechargement compte  : {2}'.format(transaction.paid_amount, transaction.number, transaction.destination_content_object)
    if flag:
        comment = 'Crédit de {0} : transaction {1}, Rechargement compte par entité {2}'.format(
            transaction.paid_amount_with_currency_of_agent_operation, transaction.number, transaction.source_content_object)
    return comment

def _get_operation_comment_of_cash_to_wallet(transaction, flag=False):
    return _get_operation_comment_of_credit_compte_entite(transaction, flag)

def _get_operation_comment_of_debit_compte_entite(transaction, flag=False):
    comment = 'Débit de {0} : transaction {1}, Débit compte  : {2}'.format(transaction.amount, transaction.number, transaction.destination_content_object)
    if flag:
        comment = 'Crédit de {0} : transaction {1}, Rechargement compte par entité {2}'.format(transaction.amount, transaction.number, transaction.source_content_object)
    return comment

def _get_operation_comment_of_wallet_to_wallet(transaction, flag=False):
    comment = 'Débit de {0} : transaction {1}, Envoi d\'argent à  : {2}'.format(transaction.amount, transaction.number, transaction.destination_content_object)
    if flag:
        comment = 'Crédit de {0} : transaction {1}, Rechargement reçu de  {2}'.format(transaction.amount, transaction.number, transaction.source_content_object)
    return comment


def _can_agent_pay_transaction(transaction, agent):
    if transaction.agent == agent:
        raise CoreException(('Operation {}'.format(transaction.number)), 'agent can not be affected to this operation')
    else:
        return True

def _can_agent_execute_transaction(source, destination):
    if source == destination:
        raise CoreException(('Entity{} is doing same operation on itself').format(source), 'This operation is done by the same agent. This'
                            ' action prohibited by the system')
    else:
        return True
