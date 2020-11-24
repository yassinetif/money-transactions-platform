import requests
import json
headers = {'Content-Type': 'application/json'}
url = 'http://217.69.6.52/api/v1/entity/agent/login/'
data = {
    "username": "test-agent",
    "password": "testpasser"
}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())

# {
#     'address': 'Dakar',
#     'code': '086796',
#     'created': '2020-03-21T13:32:44.739694',
#     'entity': {'account_number': '913296985',
#                'address': 'Dakar', 'brand_name': 'KBS',
#                'category': 'DISTRIBUTEUR',
#                'code': '761570',
#                'country': 'SN',
#                'email': 'williamsko89@gmail.com',
#                'id': 4, 'parent': 3,
#                'phone_number': '0000000',
#                'status': True},
#     'id': 1, 'phone_number': '0000000',
#     'response_code': '000',
#     'resource_uri': '/api/v1/entity/agent/1/',
#     'token': ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6'
#               'MSwiY29kZSI6IjA4Njc5NiIsI'
#               'mV4cCI6MTU4OTAyOTAxOH0.0dDuloR8eE-vXeEb'
#               'riFsaS73zSstgHpo2qosohbZhQQ'),
#     'updated': '2020-04-13T13: 00: 48.725319'
# }
