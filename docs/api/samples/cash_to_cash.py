import requests
import json

# Cash to Cash
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/entity/agent/login/'
payload = {'source_content_object': {'first_name': 'Williams', 'last_name': 'de SOUZA', 'phone_number': '773453810', 'address': 'Dakar',
                                     'identification_number': 'EB012412312', 'identification_type': 'PP', 'issuer_country': 'TG'},
           'destination_content_object': {'first_name': 'Akpene', 'last_name': 'WONU', 'phone_number': '90909333', 'address': 'Lome'}, 'type': 'CASH_TO_CASH',
           'agent': {'code': '086796'}, 'source_countr': 'SN', 'destination_country': 'TG', 'amount': '15000', 'paid_amount': '15300'}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
