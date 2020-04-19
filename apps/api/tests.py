import requests
import json
headers = {'Content-Type': 'application/json'}

# Login
url = 'http://127.0.0.1:8000/api/v1/entity/agent/login/'
data = {'username': 'a', 'password': 'semperFidelis@1989'}
response = requests.post(url, data=json.dumps(data), headers=headers)
response.json()


# Cash to Cash
payload = {'source_content_object': {'first_name': 'Williams', 'last_name': 'de SOUZA', 'phone_number': '773453810', 'address': 'Dakar',
                                     'identification_number': 'EB012412312', 'identification_type': 'PP', 'issuer_country': 'TG'},
           'destination_content_object': {'first_name': 'Akpene', 'last_name': 'WONU', 'phone_number': '90909333', 'address': 'Lome'}, 'type': 'CASH_TO_CASH',
           'agent': {'code': '086796'}, 'source_country': 'SN', 'destination_country': 'TG', 'amount': '15000', 'paid_amount': '15300'}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
response.json()

# Search code
payload = {'code': '03681479', 'agent': {'code': '086796'}}
url = 'http://127.0.0.1:8000/api/v1/transaction/search/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
response.json()

# Pay cash to cash transactions
payload = {'code': '03681479', 'agent': {'code': '086796'}, 'type': 'RETRAIT_CASH','paid_amount': '15000'}
url = 'http://127.0.0.1:8000/api/v1/transaction/pay/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
response.json()
