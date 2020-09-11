import requests
import json

# Cash to Cash
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiY29kZSI6IjY2NTQ5MyIsImV4cCI6MTU5OTI0NDk0NH0.Q9szt49_PIK4GVxgSMYhzjUxouNg6H5u1uhGjcCEusQ'

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
    "type": "CASH_TO_CASH",
    "source_country": "SN",
    "destination_country": "SN",
    "amount": "1000",
    "motif_envoi": "salaire",
    "source_revenu": "salaire"
    #"payer" : "667535"
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())

# {
#     "source_content_object": {
#         "first_name": "Elma",
#         "last_name": "Gomes",
#         "phone_number": "955497774",
#         "address": "Bairro Ajuda, Predio",
#         "identification_number": "1A1000234",
#         "identification_type": "1",
#         "issuer_country": "SN",
#         "identification_document_delivery_date": "2019-06-30",
#         "identification_document_expiry_date": "2024-06-30"
#     },
#     "destination_content_object": {
#         "first_name": "Emmanuel Ampa Emitai",
#         "last_name": "SAGNA",
#         "phone_number": "+221771589608",
#         "address": "DAKAR"
#     },
#     "type": "CASH_TO_CASH",
#     "source_country": "SN",
#     "destination_country": "SN",
#     "amount": "1000",
#     "source_revenu": "2",
#     "motif_envoi": "3"
# }
