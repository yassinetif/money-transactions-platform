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
        "first_name": "Williams",
        "last_name": "de SOUZA",
        "phone_number": "773453810",
        "address": "Dakar",
        "identification_number": "EB012412312",
        "identification_type": "PP",
        "issuer_country": "TG",
        "identification_document_deleivery_date": "2007-12-12",
        "identification_document_expiry_date": "2022-12-12"
    },
    "destination_content_object": {
        "phone_number": "788655434"
    },
    "type": "CASH_TO_WALLET",
    "amount": "70000",
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())

# {
#     "agent": {
#         "code": "086796"
#     },
#     "amount": "70000",
#     "destination_content_object": {
#         "phone_number": "788655434"
#     },
#     "destination_country": "SN",
#     "paid_amount": "70700.00",
#     "receipt_code": "44638661",
#     "source_content_object": {
#         "address": "Dakar",
#         "first_name": "Williams",
#         "identification_document_deleivery_date": "2007-12-12",
#         "identification_document_expiry_date": "2022-12-12",
#         "identification_number": "EB012412312",
#         "identification_type": "PP",
#         "issuer_country": "TG",
#         "last_name": "de SOUZA",
#         "phone_number": "773453810"
#     },
#     "source_country": "SN",
#     "transaction_number": "7629185250",
#     "type": "CASH_TO_WALLET"
# }
