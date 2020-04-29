import pytest
from kyc.repository.kyc_repository import CustomerRepository
from tests.fixtures.kyc_fixture import customer
from core.errors import CustomerException


@pytest.mark.django_db
class TestKycRepository:

    def test_fetch_or_create_customer_success(self):
        payload = {'phone_number': '11111',
                   'first_name': 'TEST', 'last_name': 'TEST'}
        result = CustomerRepository.fetch_or_create_customer(payload)
        assert result.informations.username == '11111'
        assert result.informations.first_name == 'TEST'
        assert result.informations.last_name == 'TEST'

    def test_fetch_or_create_customer_fail(self):
        payload = {'random_key': '11111',
                   'first_name': 'TEST', 'last_name': 'TEST'}
        with pytest.raises(CustomerException) as e:
            CustomerRepository.fetch_or_create_customer(payload)

        assert str(e.value) == 'CustomerException'

    def test_fetch_customer_by_phone_number_sucess(self, customer):
        phone_number = '777777'
        result = CustomerRepository.fetch_customer_by_phone_number(
            phone_number)
        assert result == customer

    def test_fetch_customer_by_phone_number_fail(self, customer):
        phone_number = '111111'
        with pytest.raises(CustomerException) as e:
            CustomerRepository.fetch_customer_by_phone_number(
                phone_number)
        assert str(e.value) == 'CustomerException 111111'
