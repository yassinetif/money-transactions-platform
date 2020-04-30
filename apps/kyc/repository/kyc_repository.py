from kyc.models import Customer
from django.contrib.auth.models import User
from core.errors import CustomerException
from shared.repository.shared_repository import SharedRepository


class CustomerRepository():

    @staticmethod
    def fetch_or_create_customer(payload):
        try:
            data = payload.copy()
            user, created = User.objects.get_or_create(
                **{'username': data.pop('phone_number'),
                   'first_name': data.pop('first_name'),
                   'last_name': data.pop('last_name')})
            payload_country = data.pop('issuer_country', None)
            issuer_country = None
            if payload_country:
                issuer_country = SharedRepository.fetch_country_by_iso(payload_country)
            data.update({'issuer_country': issuer_country})
            customer, created = Customer.objects.update_or_create(informations=user, defaults=data)
            return customer
        except Exception:
            raise CustomerException('CustomerException', 'unable to create this customer in the system')

    @staticmethod
    def fetch_customer_by_phone_number(phone_number):
        try:
            return Customer.objects.get(informations__username=phone_number)
        except Exception:
            raise CustomerException('CustomerException {0}'.format(phone_number), 'unable to find customer with phone number {0}'.format(phone_number))
