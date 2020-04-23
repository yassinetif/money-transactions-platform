import rstr
from enum import Enum
import json


def random_code(len) -> str:
    return rstr.digits(len)


def convert_enum_to_tuple(enum: Enum):
    return tuple([prefix.value for idp, prefix in enumerate(enum)])


def convert_partner_cash_to_cash_payload(base_payload: dict, partner_payload: dict):
    result = base_payload.copy()
    for key in base_payload:
        if not isinstance(base_payload.get(key), dict):
            result.update({key: partner_payload.get(base_payload.get(key))})
        else:
            data = convert_partner_cash_to_cash_payload(
                base_payload.get(key), partner_payload)
            result.update({key: data})
    return result
