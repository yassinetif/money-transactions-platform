import requests
import json
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/customer/wallet/password/'
data = {
    "phone_number": "788655434",
    "otp": "661504",
    "password": "1111"
}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())

# {
#     'phone_number': '788655434',
#     'status': True,
#     'updated': '2020-05-21T19:08:37.105750',
#     'identification_number': '245345345',
#     'created': '2020-05-21T19:08:01.008877',
#     'identification_type': 'PP',
#     'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiY29kZS'
#     'I6Ijc4ODY1NTQzNCIsImV4cCI6MTU5MjY4MDExN30.-ksBSNH31p_AcWs3'
#     'PtBl6FJNl6i55_9z1nLjvM-cVu8',
#     'identification_document_deleivery_date': '2012-12-12',
#     'response_code': '000',
#     'address': 'Dakar',
#     'identification_document_expiry_date': '2022-12-12',
#     'id': 2, 'resource_uri': '/api/v1/customer/2/'
# }
