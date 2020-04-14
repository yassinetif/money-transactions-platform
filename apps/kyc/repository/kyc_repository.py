from kyc.models import Customer
from django.contrib.auth.models import User
from core.errors import CustomerException
from shared.repository.shared_repository import SharedRepository


class CustomerRepository():

    @staticmethod
    def fetch_or_create_customer(payload):
        try:
            user, created = User.objects.get_or_create(**{'username': payload.get('identification_number'),
                                                          'first_name': payload.pop('first_name'),
                                                          'last_name': payload.pop('last_name')})
            issuer_country = SharedRepository.fetch_country_by_iso(
                payload.pop('issuer_country'))
            customer, created = Customer.objects.get_or_create(
                informations=user, issuer_country=issuer_country, **payload)
            return customer
        except Exception as err:
            raise CustomerException('unable to get or create', str(err))
