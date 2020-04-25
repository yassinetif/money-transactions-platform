
import pytest
from transaction.models import Transaction
from tests.fixtures.entity_fixture import entity, agent
from tests.fixtures.kyc_fixture import customer
from tests.fixtures.shared_fixture import country



@pytest.fixture
@pytest.mark.django_db
def transaction(agent,customer,country):

    transaction = Transaction()
    transaction.transaction_type = 'CASH_TO_CASH'
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
