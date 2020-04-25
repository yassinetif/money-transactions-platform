import pytest
from django.contrib.auth.models import User
from kyc.models import Customer


@pytest.fixture
def customer():

    user = User(**{
        'username': '777777',
        'password': 'password',
        'email': 'test@example1.com',
    })
    user.save()

    customer = Customer(**{
        'phone_number': '777777',
        'address': 'TEST',
    })
    customer.informations = user
    customer.save()
    return customer
