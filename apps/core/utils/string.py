import rstr


def random_code(len):
    return rstr.digits(len)


def convert_enum_to_tuple(enum):
    return tuple([prefix.value for idp, prefix in enumerate(enum)])


def convert_partner_cash_to_cash_payload(base_payload, partner_payload):
    result = base_payload.copy()
    for key in base_payload:
        if not isinstance(base_payload.get(key), dict):
            result.update({key: partner_payload.get(base_payload.get(key))})
        else:
            data = convert_partner_cash_to_cash_payload(
                base_payload.get(key), partner_payload)
            result.update({key: data})
    return result
