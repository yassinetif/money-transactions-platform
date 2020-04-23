from transaction.domain import partners_config
from core.errors import TransactionNotFoundException
import requests
import json


def search_transaction(payload: dict):
    configs = partners_config.WORLD_REMIT
    params = {"wr_transaction_number": payload.get('code')}
    headers = configs.get('production').get('credentials').get('headers')
    response = requests.get(configs.get('url'), params=params, headers=headers)
    if response.status_code == 200:
        pass

    else:
        raise TransactionNotFoundException(
            'No transaction Wr is found', 'No transaction is found')
