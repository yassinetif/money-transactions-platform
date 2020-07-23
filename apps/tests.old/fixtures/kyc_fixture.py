import pytest
from django.contrib.auth.models import User
from apps.kyc.models import Customer
from tests.fixtures.shared_fixture import country

@pytest.fixture
def customer(country):

    user = User(**{
        'username': '777777',
        'password': 'password',
        'email': 'test@example1.com',
        'first_name': 'TEST',
        'last_name': 'TEST'
    })
    user.save()

    customer = Customer(**{
        'phone_number': '777777',
        'address': 'TEST',
        'identification_number': 'TEST',
        'identification_type': 'TEST'
    })
    customer.informations = user
    customer.save()
    customer.issuer_country = country
    return customer
