import rstr
import secrets
import oath
from backend.settings import OTP_SECRET_KEY
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

import os
import binascii

def random_code(len):
    return rstr.digits(len)

def random_code_and_number_for_entity():
    return int(binascii.hexlify(os.urandom(3)), 16)


def convert_enum_to_tuple(enum):
    return tuple([prefix.value for idp, prefix in enumerate(enum)])

def recursive_get_data_from_payload(payload, key):
    result = payload
    for items in key.split('.'):
        result = result.get(items)
    return result


def convert_partner_cash_to_cash_payload(base_payload, partner_payload):
    result = base_payload.copy()
    for key in base_payload:
        if not isinstance(base_payload.get(key), dict):
            result.update({key: recursive_get_data_from_payload(partner_payload, base_payload.get(key))})
        else:
            data = convert_partner_cash_to_cash_payload(
                base_payload.get(key), partner_payload)
            result.update({key: data})
    return result


def convert_snake_to_camel_case(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

def generate_secret_key(len=16):
    return secrets.token_hex(len)

def format_decimal_with_two_digits_after_comma(number):
    return "%.2f" % number

def generate_totp(period=3600):
    totp = oath.totp(OTP_SECRET_KEY, format='dec6', period=period)
    return totp

def verify_totp(totp):
    return oath.accept_totp(OTP_SECRET_KEY, totp, format='dec6', period=3600)[0]


def validate_calculation_expression(expression):
    try:
        sharing_expression = expression.split('=>')[1]
        for sharing_plan in sharing_expression.split("#"):
            revenue = 0
            for _s in sharing_plan.split(';'):
                expr = _s.split(':')
                sens = expr[2]
                if sens == '-':
                    revenue -= Decimal(expr[1])
                else:
                    revenue += Decimal(expr[1])
            if revenue != 1:
                raise ValidationError(_('Sum must equal 1 . Value {0}'.format(revenue)))
    except Exception as err:
        raise ValidationError(err)

def convert_sharing_calculation_expression_to_json(expression):
    result = {}
    _expression = expression.split('=>')
    sharing_expression = _expression[1]
    for sharing_plan in sharing_expression.split("#"):
        for _s in sharing_plan.split(';'):
            expr = _s.split(':')
            entity = expr[0]
            sens = expr[2]
            value = expr[1]
            result.update({entity: '{}{}'.format(sens, value)})
    result.update({'fee': _expression[0]})
    return result

def entity_logo_directory_path(instance, filename):
    return 'entity_{0}/logo.png'.format(slugify(instance.brand_name))
