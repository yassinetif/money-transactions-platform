import requests
import json

headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/customer/wallet/create/'
payload = {
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "9099839012",
    "address": "Dakar",
    "identification_number": "245345345",
    "identification_type": "PP",
    "issuer_country": "TG",
    'email': 'test@gmail.com',
    "country": "SN",
    "identification_document_delivery_date": "2012-12-12",
    "identification_document_expiry_date": "2022-12-12"
}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())

# {
#     "address": "Dakar",
#     "country": "SN",
#     "first_name": "Sepopo",
#     "identification_document_deleivery_date": "2012-12-12",
#     "identification_document_expiry_date": "2022-12-12",
#     "identification_number": "245345345",
#     "identification_type": "PP",
#     "issuer_country": "TG",
#     "last_name": "APEH",
#     "phone_number": "788655434",
#     "response_code": "000"
# }
