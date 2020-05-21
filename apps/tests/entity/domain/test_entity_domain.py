from unittest.mock import patch
import pytest
from tests.fixtures.entity_fixture import entity_payload, entity, agent
from apps.entity.domain.entity_domain import check_entity_balance,\
    get_entity_balance_by_agent, get_entity_balance, credit_entity, debit_entity
from apps.core.errors import CoreException


class TestEntityDomain:

    @pytest.mark.django_db
    def test_get_entity_balance_by_agent(self, agent):
        result = get_entity_balance_by_agent(agent)
        assert result == 0

    @pytest.mark.django_db
    def test_get_entity_balance(self, entity):
        result = get_entity_balance(entity)
        assert result == 0

    @pytest.mark.django_db
    @patch('entity.domain.entity_domain.get_entity_balance_by_agent')
    def test_check_entity_balance_success(self, mock_get_entity_balance_by_agent, agent):
        mock_get_entity_balance_by_agent.return_value = 5000
        result = check_entity_balance(agent, 1000)
        assert result == True

    @pytest.mark.django_db
    @patch('entity.domain.entity_domain.get_entity_balance_by_agent')
    def test_check_entity_balance_fail(self, mock_get_entity_balance_by_agent, agent):
        mock_get_entity_balance_by_agent.return_value = 500
        result = check_entity_balance(agent, 1000)
        assert result == False

    @pytest.mark.django_db
    @patch('entity.domain.entity_domain.get_entity_balance')
    def test_credit_entity_success(self, mock_get_entity_balance, entity):
        mock_get_entity_balance.return_value = 5000
        credit_entity(entity, 5000, 1000)
        assert get_entity_balance(entity) == 6000

    @pytest.mark.django_db
    @patch('entity.domain.entity_domain.get_entity_balance')
    def test_credit_entity_fail(self, mock_get_entity_balance, entity):
        mock_get_entity_balance.return_value = 5000
        with pytest.raises(CoreException) as e:
            credit_entity(entity, 5000, -500)
        assert str(e.value) == 'unable to credit entity'

    @pytest.mark.django_db
    @patch('entity.domain.entity_domain.get_entity_balance')
    def test_credit_debit_success(self, mock_get_entity_balance, entity):
        mock_get_entity_balance.return_value = 5000
        debit_entity(entity, 5000, 1000)
        assert get_entity_balance(entity) == 4000

    @pytest.mark.django_db
    @patch('entity.domain.entity_domain.get_entity_balance')
    def test_debit_entity_fail(self, mock_get_entity_balance, entity):
        mock_get_entity_balance.return_value = 5000
        with pytest.raises(CoreException) as e:
            debit_entity(entity, 5000, -500)
        assert str(e.value) == 'unable to debit entity'
