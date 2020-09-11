import requests
import json

# Cash to Cash
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiY29kZSI'\
    '6IjA4Njc5NiIsImV4cCI6MTU5MTY3MTYwMX0.cG1OgCtGa4GOxa7_cuODR'\
        'kybMXVjop11o2siAFrceHY'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}
url = 'http://127.0.0.1:8000/api/v1/customer/card/create/'
payload = {
    "customer": {
        "first_name": "Nnenne",
        "last_name": "Igwebuike",
        "phone_number": "864-208-4784",
        "address": '903 Mill StreetGreenville, SC 29601',
        "identification_number": "0483775596",
        "identification_type": "PP",
        "issuer_country": "SN",
        "country": "SN",
        "identification_document_deleivery_date": "2012-12-12",
        "identification_document_expiry_date": "2022-12-12"
    },
    "card_number": "MAM5576115925871096",
    "amount": "1500",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response)
print(response.json())

# Response

# {
#     "agent": {
#         "code": "086796"
#     },
#     "amount": "1500",
#     "card_number": "MAM5576115925871096",
#     "customer": {
#         "address": "903 Mill StreetGreenville, SC 29601",
#         "country": "SN",
#         "first_name": "Nnenne",
#         "identification_document_deleivery_date": "2012-12-12",
#         "identification_document_expiry_date": "2022-12-12",
#         "identification_number": "0483775596",
#         "identification_type": "PP",
#         "issuer_country": "SN",
#         "last_name": "Igwebuike",
#         "phone_number": "864-208-4784"
#     },
#     "destination_country": "SN",
#     "paid_amount": "1800.00",
#     "response_code": "000",
#     "source_country": "SN",
#     "type": "ACTIVATION_CARTE"
# }
