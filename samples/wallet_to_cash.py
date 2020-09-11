import requests
import json

# Wallet to Cash
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImN'\
    'vZGUiOiI3ODg2NTU0MzQiLCJleHAi'\
    'OjE1OTE3MjA0NTN9.NQOYgO25oq8WcIwZGAeLIOebn52S-Dzb6iditScRjL0'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}

payload = {
    "destination_content_object": {
        "first_name": "Akpene",
        "last_name": "WONU",
        "phone_number": "90909333",
        "address": "Lome",
        "country": "TG",
    },
    "type": "WALLET_TO_CASH",
    "amount": "80000",
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())


# {
#     "receipt_code": "89999112",
#     "paid_amount": "80393.907500000000",
#     "source_content_object": {
#         "phone_number": "788655434"
#     },
#     "source_country": "GN",
#     "transaction_number": "9046984902",
#     "destination_country": "TG",
#     "amount": "80000",
#     "type": "WALLET_TO_CASH",
#     "destination_content_object": {
#         "phone_number": "90909333",
#         "country": "TG",
#         "first_name": "Akpene",
#         "last_name": "WON",
#         "address": "Lome"
#     }
# }
