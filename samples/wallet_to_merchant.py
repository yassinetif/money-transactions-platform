import requests
import json

# Wallet to Merchant
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImN'\
    'vZGUiOiI3ODg2NTU0MzQiLCJleHAi'\
    'OjE1OTE3MjA0NTN9.NQOYgO25oq8WcIwZGAeLIOebn52S-Dzb6iditScRjL0'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}

payload = {
    "source_content_object": {
        "phone_number": "788655434",
    },
    "destination_content_object": {
        "phone_number": "788655434",
    },
    "type": "WALLET_TO_WALLET",
    "amount": "1000",
    "paid_amount": "1200"
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
