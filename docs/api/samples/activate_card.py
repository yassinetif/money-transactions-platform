import requests
import json

# Cash to Cash
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/customer/card/create/'
payload = {
    "customer": {
        "first_name": "Sepopo",
        "last_name": "APEH",
        "phone_number": "788655434",
        "address": "Dakar",
        "identification_number": "245345345",
        "identification_type": "PP",
        "issuer_country": "TG",
        "country": "SN",
        "identification_document_deleivery_date": "2012-12-12",
        "identification_document_expiry_date": "2022-12-12"
    },
    "card_number": "MAM465793Z4A5345",
    "amount": "15000",
    "paid_amount": "15300",
    "agent": {
        "code": "086796"
    }
}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print (response)
print(response.json())
