
from apps.transaction.controller.transaction_controller import _validate_transaction_payload, _get_agent_info,\
    _check_agent_balance, create_transaction, _debit_entity, insert_operation
from apps.transaction.domain.transaction_domain import calculate_transaction_paid_amount_and_fee,\
    get_fee_calculation_payload
from apps.kyc.domain.customer_domain import get_customer_balance
from tastypie.http import HttpUnauthorized, HttpForbidden
from apps.kyc.repository.kyc_repository import CustomerRepository
from apps.core.errors import CoreException
from marshmallow import ValidationError
from apps.transaction.decorator.transaction_decorator import agent_code_required
from apps.core.utils.http import get_request_token
from apps.core.utils.string import format_decimal_with_two_digits_after_comma
from django.contrib.auth.models import User
from apps.core.utils.http import create_jwt_token_for
from apps.core.utils.string import generate_totp, verify_totp
from apps.services.tasks import sms_task
from apps.core.utils.validator import WalletLoginValidator


def _validate_login_payload(payload):
    try:
        _validator = WalletLoginValidator()
        _validator.load(payload)
    except ValidationError as err:
        raise ValidationError(str(err))
    except KeyError:
        raise ValidationError('please specify username and password')


def create_customer_with_card(tastypie, payload, request):
    try:
        payload.update({'type': 'ACTIVATION_CARTE'})
        _validate_transaction_payload(payload.copy())
        token = get_request_token(request)
        result = _create_customer_with_card(payload, token)
        return tastypie.create_response(request, result)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


@agent_code_required
def _create_customer_with_card(payload, token):
    agent = _get_agent_info(payload)

    payload.update({'source_country': agent.entity.country.iso.code})
    fee_calculation_payload = get_fee_calculation_payload(payload)
    paid_amount = calculate_transaction_paid_amount_and_fee(fee_calculation_payload)[1]
    payload.update({'paid_amount': format_decimal_with_two_digits_after_comma(paid_amount)})
    _check_agent_balance(agent, payload)
    # TODO : activate_monnamon_card(payload)
    transaction = create_transaction(payload, agent)
    _debit_entity(transaction)
    insert_operation(transaction)
    payload.update({'response_code': '000'})
    return payload


def create_customer_with_wallet(tastypie, payload, request):
    try:
        data = payload.copy()
        data.update({'type': 'CREATION_WALLET'})
        _validate_transaction_payload(data)
        CustomerRepository.fetch_or_create_customer(payload)
        payload.update({'response_code': '000'})

        otp = generate_totp()
        sms_task.run(payload.get('phone_number'), otp)

        return tastypie.create_response(request, payload)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


def get_wallet_balance(tastypie, payload, request):
    try:
        data = payload.copy()
        data.update({'type': 'WALLET_BALANCE'})
        _validate_transaction_payload(data)
        customer = CustomerRepository.fetch_customer_by_phone_number(payload.get('phone_number'))
        balance = get_customer_balance(customer)
        payload.update({'response_code': '000', 'balance': balance, 'currency': customer.country.currency.iso})
        return tastypie.create_response(request, payload)
    except ValidationError as err:
        return tastypie.create_response(request, {'response_text': str(err), 'response_code': '100'}, HttpUnauthorized)
    except CoreException as err:
        return tastypie.create_response(request, err.errors, HttpForbidden)


def wallet_login(tastypie, data, request):
    try:

        _validate_login_payload(data)

        phone_number = data['phone_number']
        password = data['password']

        user = User.objects.get(username=phone_number)
        if user and user.is_active:
            result = user.check_password(password)
            if result:
                wallet = CustomerRepository.fetch_customer_by_phone_number(user, status=True)
                bundle = tastypie.build_bundle(obj=wallet, request=request)
                bundle = tastypie.full_dehydrate(bundle)
                bundle.data.update({'response_code': '000'})
                bundle.data.update({'first_name': wallet.informations.first_name})
                bundle.data.update({'last_name': wallet.informations.last_name})
                bundle.data.update(create_jwt_token_for(wallet, 'wallet_api_secret_key'))

                return tastypie.create_response(request, bundle)
            else:
                return tastypie.create_response(request, {'response_text': 'wrong password', 'response_code': '100'}, HttpForbidden)
        else:
            return tastypie.create_response(request, {'response_text': 'Inactive Wallet', 'response_code': '100'}, HttpUnauthorized)
    except User.DoesNotExist:
        return tastypie.create_response(request, {'response_text': 'unknwonw user', 'response_code': '100'}, HttpForbidden)
    except Exception as err:
        return tastypie.create_response(request, {'response_text': err, 'response_code': '100'}, HttpForbidden)


def define_wallet_password(tastypie, data, request):

    phone_number = data['phone_number']
    password = data['password']
    otp = data['otp']

    result = result = verify_totp(otp)
    if result is False:
        return tastypie.create_response(request, {'response_text': 'wrong OTP', 'response_code': '100'}, HttpUnauthorized)
    try:
        customer = CustomerRepository.fetch_customer_by_phone_number(phone_number)
        customer.informations.set_password(password)
        customer.informations.save()
        customer.status = True
        customer.save()

        bundle = tastypie.build_bundle(obj=customer, request=request)
        bundle = tastypie.full_dehydrate(bundle)
        bundle.data.update({'response_code': '000'})
        bundle.data.update(create_jwt_token_for(customer, 'wallet_api_secret_key'))

        return tastypie.create_response(request, bundle)
    except Exception:
        return tastypie.create_response(request, {'response_text': 'unable to define password ', 'response_code': '100'}, HttpForbidden)

def customer_beneficiaries(tastypie, phone_number, request):

    try:
        customer = CustomerRepository.fetch_customer_by_phone_number(phone_number)
        relations = customer.relations.all()
        beneficiaries = []

        bundle = tastypie.build_bundle(obj=customer, request=request)
        bundle = tastypie.full_dehydrate(bundle)
        bundle.data.update({'response_code': '000'})
        bundle.data.update({'customer': {'first_name': customer.informations.first_name, 'last_name': customer.informations.last_name}})
        for beneficiary in relations:
            data = {
                'first_name': beneficiary.informations.first_name,
                'last_name': beneficiary.informations.last_name,
                'phone_number': beneficiary.informations.username,
                'address': beneficiary.address
            }
            beneficiaries.append(data)
        bundle.data.update({'beneficiaries': beneficiaries})

        return tastypie.create_response(request, bundle)
    except Exception as err:
        print(err)
        return tastypie.create_response(request, {'response_text': 'no beneficiairies ', 'response_code': '100'}, HttpForbidden)
