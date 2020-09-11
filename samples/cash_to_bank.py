import requests
import json

# Cash to Cash
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI'\
    '6MiwiY29kZSI6IjY2NTQ5MyIsImV4cCI6MTU5MjY3NjQ'\
        '5OX0.fh_DohPr_AtyMheoLN8S_nssRu0GTC4VvQAJMqWQMWI'

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
        "identification_document_delivery_date": "2007-12-12",
        "identification_document_expiry_date": "2022-12-12"
    },
    "destination_content_object": {
        "first_name": "Betty",
        "last_name": "Davis",
        "phone_number": "213-633-1514",
        "address": "Lome"
    },
    "type": "CASH_TO_BANK_ACCOUNT",
    "source_country": "SN",
    "destination_country": "SN",
    "amount": "1000",
    "motif_envoi": "salaire",
    "source_revenu": "salaire",
    "bank_nane": "ECOBANK",
    "rib": "XXXXXX"
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
