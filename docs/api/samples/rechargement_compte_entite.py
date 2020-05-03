import requests
import json

# Cash to Cash
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
payload = {
    'type': 'RECHARGEMENT_COMPTE_ENTITE',
    'account_number': '913296986',
    'amount': '5000',
    'paid_amount': '5300',
    'agent': {'code': '086796'}
}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response)
print(response.json())
