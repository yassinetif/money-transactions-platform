import rstr


def random_code(len):
    return rstr.digits(len)


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


