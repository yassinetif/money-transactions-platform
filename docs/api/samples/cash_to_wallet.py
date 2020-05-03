import requests
import json

# Cash to Cash
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/entity/agent/login/'
payload = {'source_content_object': {
    'first_name': 'Williams',
    'last_name': 'de SOUZA',
    'phone_number': '773453810',
    'address': 'Dakar',
    'identification_number': 'EB012412312',
    'identification_type': 'PP',
    'issuer_country': 'TG',
    'identification_document_deleivery_date': '2007-12-12',
    'identification_document_expiry_date': '2022-12-12'},
    'destination_content_object': {
        'phone_number': '788655434'
},
    'type': 'CASH_TO_WALLET',
    'agent': {
        'code': '086796'
}, 'amount': '-5000',
    'paid_amount': '7175'
}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
