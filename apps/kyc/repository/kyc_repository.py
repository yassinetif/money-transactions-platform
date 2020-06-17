from apps.kyc.models import Customer
from django.contrib.auth.models import User
from apps.core.errors import CustomerException
from apps.shared.repository.shared_repository import SharedRepository


class CustomerRepository():

    @staticmethod
    def fetch_or_create_customer(payload, is_card_activation=False):
        try:
            data = payload.copy()
            user_info = {}
            user_info.update({'first_name': data.pop('first_name')})
            user_info.update({'last_name': data.pop('last_name')})
            user_info.update({'email': data.pop('email', 'info@monnamon.com')})
            user, created = User.objects.update_or_create(username=data.get('phone_number'), defaults=user_info)

            payload_country = data.pop('issuer_country', None)
            residence_country = data.pop('country', None)
            issuer_country = None
            country = None
            if payload_country:
                issuer_country = SharedRepository.fetch_country_by_iso(payload_country)
            if residence_country:
                country = SharedRepository.fetch_country_by_iso(residence_country)
            data.update({'issuer_country': issuer_country})
            customer, created = Customer.objects.update_or_create(informations=user, defaults=data)
            customer.country = country
            customer.save()

            SharedRepository.initialize_account(customer, created, is_card_activation)
            return customer
        except Exception as err:
            print(err)
            raise CustomerException(str(err), 'unable to create this customer in the system')

    @staticmethod
    def fetch_customer_by_phone_number(phone_number, status=True):
        try:
            return Customer.objects.get(informations__username=phone_number)
        except Customer.DoesNotExist:
            raise CustomerException('unable to find customer with phone number {}'.format(phone_number), 'CustomerException {}'.format(phone_number))
        except Exception:
            raise CustomerException('CustomerException', 'unable to find this customer in the system')

    @staticmethod
    def fetch_customer_beneficiary_by_phone_number(phone_number):
        try:
            return Customer.objects.get(informations__username=phone_number).relations().all()
        except Customer.DoesNotExist:
            raise CustomerException('unable to find customer with phone number {}'.format(phone_number), 'CustomerException {}'.format(phone_number))
        except Exception:
            raise CustomerException('CustomerException', 'unable to find this customer in the system')
