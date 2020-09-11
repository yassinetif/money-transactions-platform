import requests

# Agent OTP

headers = {'Content-Type': 'application/json'}

url = ('http: // 127.0.0.1: 8000/api/v1/customer/wallet/beneficiaries /?'
       'phone_number=716-759-2189')
response = requests.get(url, headers=headers)
print(response.json())


# {
#     "address": "Dakar",
#     "beneficiaries": [
#         {
#             "address": "Lome",
#             "first_name": "Betty",
#             "last_name": "Davis",
#             "phone_number": "213-633-1514"
#         }
#     ],
#     "created": "2020-06-15T22:03:20.561009",
#     "id": 7,
#     "identification_document_delivery_date": "2007-12-12",
#     "identification_document_expiry_date": "2022-12-12",
#     "identification_number": "EB012412312",
#     "identification_type": "PP",
#     "phone_number": "716-759-2189",
#     "resource_uri": "/api/v1/customer/7/",
#     "response_code": "000",
#     "status": false,
#     "updated": "2020-06-15T22:16:04.862580"
# }
