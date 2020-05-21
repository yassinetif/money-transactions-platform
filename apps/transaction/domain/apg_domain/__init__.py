from apps.transaction.domain import partners_config
from apps.core.errors import PartnerApiException
from apps.core.utils.string import convert_partner_cash_to_cash_payload
import requests


def activate_monnamon_card(payload):
    try:
        configs = partners_config.APG
        transaction_type = payload.get('type')
        headers = configs.get(transaction_type).get('test').get('credentials').get('headers')
        activate_apg_card_payload = convert_partner_cash_to_cash_payload(configs.get(transaction_type).get('payload'), payload)
        response = requests.post(configs.get(transaction_type).get('test').get('url'), data=activate_apg_card_payload, headers=headers)
        result = response.json()
        if result.get('code') == '000':
            return result
        else:
            raise PartnerApiException(
                'apg card activation', 'Unable to activate customer card from APG')
    except Exception:
        raise PartnerApiException('apg card activation', 'Unable to reach APG Card Activation API')
