from apps.transaction.domain import partners_config
from apps.core.errors import TransactionNotFoundException
from apps.core.utils import convert_partner_cash_to_cash_payload
import requests


def search_transaction(payload):
    configs = partners_config.WORLD_REMIT
    params = {"wr_transaction_number": payload.get('code')}
    transaction_type = payload.get('type')
    headers = configs.get(transaction_type).get('production').get('credentials').get('headers')
    response = requests.get(configs.get(transaction_type).get('url'), params=params, headers=headers)
    if response.status_code == 200:
        json_request = convert_partner_cash_to_cash_payload(
            configs.get(transaction_type).get('payload'), response.json())
        return json_request

    else:
        raise TransactionNotFoundException(
            'No transaction Wr is found', 'No transaction is found')
