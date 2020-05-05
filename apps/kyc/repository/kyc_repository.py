from kyc.models import Customer
from django.contrib.auth.models import User
from core.errors import CustomerException
from shared.repository.shared_repository import SharedRepository


class CustomerRepository():

    @staticmethod
    def fetch_or_create_customer(payload, is_card_activation=False):
        try:
            data = payload.copy()
            user_info = {}
            user_info.update({'first_name': data.pop('first_name')})
            user_info.update({'last_name': data.pop('last_name')})
            user, created = User.objects.update_or_create(username=data.pop('phone_number'), defaults=user_info)

            payload_country = data.pop('issuer_country', None)
            residence_country = data.pop('country', None)
            issuer_country = None
            country = None
            print('user', user.first_name)
            if payload_country:
                issuer_country = SharedRepository.fetch_country_by_iso(payload_country)
            if residence_country:
                country = SharedRepository.fetch_country_by_iso(residence_country)
            data.update({'issuer_country': issuer_country})
            print (data)
            customer, created = Customer.objects.update_or_create(informations=user, country=country, defaults=data)

            SharedRepository.initialize_account(customer, created, is_card_activation)
            return customer
        except Exception as err:
            print (err)
            raise CustomerException('CustomerException', 'unable to create this customer in the system')

    @staticmethod
    def fetch_customer_by_phone_number(phone_number):
        try:
            return Customer.objects.get(informations__username=phone_number)
        except Exception:
            raise CustomerException('CustomerException {0}'.format(phone_number), 'unable to find customer with phone number {0}'.format(phone_number))
