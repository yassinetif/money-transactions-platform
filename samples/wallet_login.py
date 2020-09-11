import requests
import json
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/customer/wallet/login/'
data = {
    "phone_number": "788655434",
    "password": "1111"
}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())

# {
#     "address": "Dakar",
#     "created": "2020-05-03T00:27:05.889925",
#     "id": 14,
#     "identification_document_deleivery_date": "2012-12-12",
#     "identification_document_expiry_date": "2022-12-12",
#     "identification_number": "245345345",
#     "identification_type": "PP",
#     "phone_number": "788655434",
#     'authentication_type': 'DEFAULT' (ou OTP)
#     "response_code": "000",
#     "resource_uri": "/api/v1/customer/14/",
#     "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImNvZG
# UiOiI3ODg2NTU0MzQiLCJleHAiOjE1OTE3MjA0NTN9.NQOY
# gO25oq8WcIwZGAeLIOebn52S-Dzb6iditScRjL0",
#     "updated": "2020-05-10T14:22:58.141992"
# }
