
import pytest
from transaction.models import Transaction
from tests.fixtures.entity_fixture import entity, agent
from tests.fixtures.kyc_fixture import customer
from tests.fixtures.shared_fixture import country


@pytest.fixture
def transaction_cash_to_cash_payload():
    return {'source_content_object': {'first_name': 'Williams', 'last_name': 'de SOUZA', 'phone_number': '773453810', 'address': 'Dakar',
                                      'identification_number': 'EB012412312', 'identification_type': 'PP', 'issuer_country': 'TG'},
            'destination_content_object': {'first_name': 'Akpene', 'last_name': 'WONU', 'phone_number': '90909333', 'address': 'Lome'}, 'type': 'CASH_TO_CASH',
            'agent': {'code': '086796'}, 'source_country': 'SN', 'destination_country': 'SN', 'amount': '5000', 'paid_amount': '5300'}


@pytest.fixture
def transaction(agent, customer, country):

    transaction = Transaction()
    transaction.transaction_type = 'CASH_TO_CASH'
    transaction.number = 'TEST_NUMBER'
    transaction.code = 'TEST_CODE'
    transaction.agent = agent
    transaction.amount = 15000
    transaction.paid_amount = 15300
    transaction.source_content_object = customer
    transaction.destination_content_object = customer
    transaction.source_country = country
    transaction.destination_country = country
    transaction.save()
    return transaction