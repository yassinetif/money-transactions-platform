import requests
import json

# Wallet to Wallet
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImN'\
    'vZGUiOiI3ODg2NTU0MzQiLCJleHAi'\
    'OjE1OTE3MjA0NTN9.NQOYgO25oq8WcIwZGAeLIOebn52S-Dzb6iditScRjL0'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}
payload = {
    "destination_content_object": {
        "phone_number": "864-208-4784",
    },
    "type": "WALLET_TO_WALLET",
    "amount": "1000",
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())

# {
#     "amount": "1000",
#     "destination_content_object": {
#         "phone_number": "864-208-4784"
#     },
#     "destination_country": "SN",
#     "paid_amount": "1787.815000000000",
#     "receipt_code": "87042332",
#     "source_content_object": {
#         "phone_number": "788655434"
#     },
#     "source_country": "GN",
#     "transaction_number": "1904652090",
#     "type": "WALLET_TO_WALLET"
# }
