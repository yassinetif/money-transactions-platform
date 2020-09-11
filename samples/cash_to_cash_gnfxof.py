import requests
import json

# Cash to Cash
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiY29kZSI6Ijc'\
    '4NjI2NyIsImV4cCI6MTU5MTY3MTc0N30.XX3gz'\
        '5wyKxR4Lvapd4kl4bJBeaj0XSEr_Neb19PyGhA'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}
payload = {
    "source_content_object": {
        "first_name": "Denise",
        "last_name": "Benoit",
        "phone_number": "716-759-2189",
        "address": "Dakar",
        "identification_number": "EB012412312",
        "identification_type": "PP",
        "issuer_country": "TG",
        "identification_document_deleivery_date": "2007-12-12",
        "identification_document_expiry_date": "2022-12-12"
    },
    "destination_content_object": {
        "first_name": "Betty",
        "last_name": "Davis",
        "phone_number": "213-633-1514",
        "address": "Lome"
    },
    "type": "CASH_TO_CASH",
    "source_country": "GN",
    "destination_country": "SN",
    "amount": "800000",
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
