from marshmallow import ValidationError
import pytest
from unittest.mock import patch
from tests.fixtures.entity_fixture import entity, agent
from tests.fixtures.shared_fixture import country, grille_tarifaire, corridor
from tests.fixtures.kyc_fixture import customer
from tests.fixtures.transaction_fixture import transaction_cash_to_cash_payload, transaction, dumped_transaction_cash_to_cash_payload
from apps.transaction.controller.transaction_controller import _validate_transaction_payload, _dump_transaction_payload,\
    _validate_search_transaction_by_code_payload, _get_agent_info, _check_agent_balance
from apps.core.errors import AgentException, CoreException


@pytest.mark.django_db
class TestTransactionController:

    def test_validate_transaction_payload_success(self, transaction_cash_to_cash_payload):
        result = _validate_transaction_payload(transaction_cash_to_cash_payload)
        assert result is None

    def test_validate_transaction_payload_fail_with_no_source_country(self, transaction_cash_to_cash_payload):
        del transaction_cash_to_cash_payload['source_country']
        with pytest.raises(ValidationError) as err:
            result = _validate_transaction_payload(transaction_cash_to_cash_payload)
            assert result is None
        assert str(err.value) == "{'source_country': ['Missing data for required field.']}"

    def test_dump_transaction_payload_success(self, transaction, grille_tarifaire, dumped_transaction_cash_to_cash_payload):
        transaction.grille = grille_tarifaire
        result = _dump_transaction_payload(transaction)
        assert result == dumped_transaction_cash_to_cash_payload

    def test_dump_transaction_payload_success(self, transaction, grille_tarifaire, transaction_cash_to_cash_payload):
        transaction.grille = grille_tarifaire
        result = _dump_transaction_payload(transaction)
        assert result != transaction_cash_to_cash_payload

    def test_validate_search_transaction_by_code_payload_success(self):
        payload = {'code': 'WR14636702', 'agent': {'code': '086796'}}
        result = _validate_search_transaction_by_code_payload(payload)
        assert result is None

    def test_validate_search_transaction_by_code_payload_failed_with_agent_not_in_payload(self):
        payload = {'code': 'WR14636702'}
        with pytest.raises(ValidationError) as err:
            result = _validate_search_transaction_by_code_payload(payload)
            assert result is None
        assert str(err.value) == "{'agent': ['Missing data for required field.']}"


    def test_get_agent_info_fail_with_wrong_agent_code(self, transaction_cash_to_cash_payload, agent):
        transaction_cash_to_cash_payload.update({'agent':{'code':'45454'}})
        with pytest.raises(AgentException) as err:
            result = _get_agent_info(transaction_cash_to_cash_payload)
            assert result != agent
        assert str(err.value) == 'unknown agent account'

    def test_check_agent_balance_fail_balance_not_enough(self, transaction_cash_to_cash_payload, agent):
        with pytest.raises(CoreException) as err:
            _check_agent_balance(agent, transaction_cash_to_cash_payload)
        assert str(err.value) == 'agent does not have enough balance'

    def test_debit_entity(self):
        # TODO
        pass

    def test_credit_entity(self):
        # TODO
        pass

    def test_addtitional_transactions_informations(self):
        # TODO
        pass

    def test_addtitional_customer_informations(self):
        # TODO
        pass

    def test_create(self):
        # TODO
        pass

    def test_search(self):
        # TODO
        pass

    def test_pay(self):
        # TODO
        pass

    def test_get_validator_class(self):
        # TODO
        pass
