import pytest
from mock import patch
from tests.fixtures.shared_fixture import grille_tarifaire, corridor, country
from tests.fixtures.entity_fixture import entity, agent, entity_child, other_agent
from tests.fixtures.kyc_fixture import customer
from tests.fixtures.transaction_fixture import transaction_cash_to_cash_payload, transaction
from transaction.domain.transaction_domain import get_grille_tarifaire, debit_entity_account,\
    credit_entity_account, create_transaction, get_partner_module_name, search_transaction,\
    pay_transaction, _can_agent_pay_transaction, _get_operation_comment
from shared.models.price import FeeType
from core.errors import GrilleException, CoreException, CountryException, TransactionNotFoundException


@pytest.mark.django_db
class TestTransactionDomain:

    def test_get_grille_tarifaire_success(self, grille_tarifaire):
        payload = {'amount': 1500, 'source_country': 'SN',
                   'destination_country': 'SN', 'type': 'CASH_TO_CASH'}
        result = get_grille_tarifaire(payload)
        assert result != None
        assert result.fee_type == FeeType.CONST.value
        assert result.fee == 500

    def test_get_grille_tarifaire_fail(self, grille_tarifaire):
        payload = {'amount': 10000000000000, 'source_country': 'SN',
                   'destination_country': 'SN', 'type': 'CASH_TO_CASH'}

        with pytest.raises(GrilleException) as e:
            get_grille_tarifaire(payload)
        assert str(e.value) == 'grille error'

    @patch('entity.domain.entity_domain.debit_entity')
    def test_debit_entity_account_fail(self, mock_debit_entity, agent):
        mock_debit_entity.side_effect = CoreException(
            'unable to debit entity', 'transaction failed')

        with pytest.raises(CoreException) as e:
            debit_entity_account(agent, 0, -1000)
        assert str(e.value) == 'unable to debit entity'

    @patch('entity.domain.entity_domain.credit_entity')
    def test_credit_entity_account_fail(self, mock_credit_entity, agent):
        mock_credit_entity.side_effect = CoreException(
            'unable to credit entity', 'transaction failed')

        with pytest.raises(CoreException) as e:
            credit_entity_account(agent, 0, -1000)
        assert str(e.value) == 'unable to credit entity'

    @patch('kyc.repository.kyc_repository.CustomerRepository.fetch_or_create_customer')
    @patch('shared.repository.shared_repository.SharedRepository.fetch_country_by_iso')
    def test_create_transaction_cash_to_cash_success(self, mock_fetch_country_by_iso, mock_fetch_or_create_customer,
                                                     transaction_cash_to_cash_payload,
                                                     agent, customer, grille_tarifaire, country):
        mock_fetch_or_create_customer.return_value = customer
        mock_fetch_country_by_iso.return_value = country
        result = create_transaction(transaction_cash_to_cash_payload, agent)
        assert result != None
        assert result.transaction_type == 'CASH_TO_CASH'
        assert result.amount == '5000'
        assert result.paid_amount == '5300'
        assert result.source_country.iso == 'SN'
        assert result.destination_country.iso == 'SN'
        assert result.source_content_object == customer
        assert result.destination_content_object == customer

    @patch('kyc.repository.kyc_repository.CustomerRepository.fetch_or_create_customer')
    @patch('shared.repository.shared_repository.SharedRepository.fetch_country_by_iso')
    @patch('transaction.domain.transaction_domain')
    def test_create_transaction_cash_to_cash_raises_grille_error(self, mock_transaction_domain, mock_fetch_country_by_iso, mock_fetch_or_create_customer,
                                                                 transaction_cash_to_cash_payload,
                                                                 agent, customer, country, corridor):
        mock_fetch_or_create_customer.return_value = customer
        mock_fetch_country_by_iso.return_value = country
        mock_transaction_domain.get_grille_tarifaire.side_effect = GrilleException(
            'grille error', 'error')

        with pytest.raises(GrilleException) as e:
            result = create_transaction(
                transaction_cash_to_cash_payload, agent)
            assert result == None
        assert str(e.value) == 'grille error'

    @patch('kyc.repository.kyc_repository.CustomerRepository.fetch_or_create_customer')
    @patch('shared.repository.shared_repository.SharedRepository.fetch_country_by_iso')
    def test_create_transaction_cash_to_cash_raises_country_error(self, mock_fetch_country_by_iso, mock_fetch_or_create_customer,
                                                                  transaction_cash_to_cash_payload,
                                                                  agent, customer, grille_tarifaire):
        mock_fetch_or_create_customer.return_value = customer
        mock_fetch_country_by_iso.side_effect = CountryException(
            'country error', 'error')

        with pytest.raises(CountryException) as e:
            result = create_transaction(
                transaction_cash_to_cash_payload, agent)
            assert result == None
        assert str(e.value) == 'country error'

    def test_get_partner_module_name_success(self):
        code = 'WR'
        result = get_partner_module_name(code)
        assert result == 'transaction.domain.world_remit_domain'

    def test_get_partner_module_name_fail(self):
        code = 'FAKE'
        result = get_partner_module_name(code)
        assert result == None

    def test_search_transaction_unpaid_success(self, transaction):
        code = 'TEST_CODE'
        payload = {'code': code}
        result = search_transaction(payload)
        assert result == transaction
        assert result.code == code
        assert result.status == 'PENDING'

    def test_search_transaction_unpaid_fail(self, transaction):
        code = 'TEST_CODE'
        payload = {'code': code}
        transaction.status = 'PAID'
        transaction.save()
        with pytest.raises(TransactionNotFoundException) as e:
            result = search_transaction(payload)
            assert result == None
        assert str(e.value) == 'unavailable transaction code'

    def test_pay_transaction_with_same_agent_raise_exception(self, transaction, agent):
        payload = {'code': 'TEST_CODE', 'agent': {'code': 'AGENT_CODE'}}
        with pytest.raises(CoreException) as e:
            result = pay_transaction(payload, agent)
            assert result == None
        assert str(e.value) == 'agent can not be affected to this operation'

    def test_pay_transaction_success(self, transaction, other_agent):
        payload = {'code': 'TEST_CODE', 'agent': {'code': 'AUTRE_AGENT'}}
        result = pay_transaction(payload, other_agent)
        assert result != None
        assert result.parent_transaction_number != None
        assert result.status == 'SUCCESS'

    def test_can_agent_pay_transaction_sucess(self, transaction, other_agent):
        result = _can_agent_pay_transaction(transaction, other_agent)
        assert result == True

    def test_can_agent_pay_transaction_fail(self, transaction, agent):
        with pytest.raises(CoreException) as e:
            result = _can_agent_pay_transaction(transaction, agent)
            assert result == None
        assert str(e.value) == 'agent can not be affected to this operation'

    def test_get_operation_comment_cash_to_cash(self, transaction):
        expected = 'Débit de 15300 : transaction TEST_NUMBER'
        result = _get_operation_comment(transaction)
        assert result == expected

    def test_get_operation_comment_retrait_cash(self, transaction):
        transaction.transaction_type = 'RETRAIT_CASH'
        transaction.save()

        expected = 'Crédit de 15000 : transaction TEST_NUMBER'
        result = _get_operation_comment(transaction)
        assert result == expected

    def test_calculate_transaction_fee(self):
        pass
        # TODO

    def test_currency_change(self):
        pass
        # TODO
