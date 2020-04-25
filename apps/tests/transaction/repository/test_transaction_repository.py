import pytest
from tests.fixtures.transaction_fixture import transaction
from transaction.repository.transaction_repository import TransactionRepository
from tests.fixtures.entity_fixture import entity, agent
from tests.fixtures.kyc_fixture import customer
from tests.fixtures.shared_fixture import country
from core.errors import TransactionNotFoundException


@pytest.mark.django_db
class TestTransactionRepository:

    def test_fetch_unpaid_transaction_by_code_success(self, transaction):
        code = 'TEST_CODE'
        result = TransactionRepository.fetch_unpaid_transaction_by_code(code)
        assert result.number == transaction.number
        assert result.source_content_object == transaction.source_content_object
        assert result.destination_content_object == transaction.destination_content_object
        assert result.agent == transaction.agent
        assert result.amount == transaction.amount
        assert result.paid_amount == transaction.paid_amount

    def test_fetch_unpaid_transaction_by_code_fail(self, transaction):
        code = 'FAIL_CODE'
        with pytest.raises(TransactionNotFoundException) as e:
            TransactionRepository.fetch_unpaid_transaction_by_code(code)
        assert str(e.value) == 'unavailable transaction code'
