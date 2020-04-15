import requests
import json
headers = {'Content-Type': 'application/json'}

# Login
url = 'http://127.0.0.1:8000/api/v1/entity/agent/login/'
data = {'username': 'a', 'password': 'semperFidelis@1989'}
response = requests.post(url, data=json.dumps(data), headers=headers)
response.json()


# Cash to Cash
payload = {'sender': {'first_name': 'Williams', 'last_name': 'de SOUZA', 'phone_number': '773453810', 'address': 'Dakar',
                      'identification_number': 'EB012412312', 'identification_type': 'PP', 'issuer_country': 'TG'},
           'receiver': {'first_name': 'Astrid Laurce', 'last_name': 'Kengueleoua', 'phone_number': '778433205', 'address': 'Dakar',
                        'identification_number': '4351245EFSDF', 'identification_type': 'PP', 'issuer_country': 'SN'}, 'type': 'CASH_TO_CASH',
           'agent': {'code': '086796'}, 'source_country': 'SN', 'destination_country': 'SN', 'amount': 5000, 'paid_amount': 5000}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
response.json()

# Search code
payload = {'code': '96316472', 'agent': {'code': '086796'}}
url = 'http://127.0.0.1:8000/api/v1/transaction/search/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
response.json()
