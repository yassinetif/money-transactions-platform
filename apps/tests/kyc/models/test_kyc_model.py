import pytest
from tests.fixtures.kyc_fixture import customer
from tests.fixtures.shared_fixture import country

@pytest.mark.django_db
class TestKyc:

    def test_kyc_exists(self, customer):
        assert customer.pk == 1
