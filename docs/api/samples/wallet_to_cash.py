import requests
import json

# Cash to Cash
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/entity/agent/login/'
payload = {
    "source_content_object": {
        "phone_number": "788655434",
    },
    "destination_content_object": {
        "first_name": "Akpene",
        "last_name": "WONU",
        "phone_number": "90909333",
        "address": "Lome",
        "country": "TG",
    },
    "type": "WALLET_TO_CASH",
    "amount": "1000",
    "paid_amount": "1200"
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
