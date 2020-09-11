import requests
import json
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiY29kZSI6Ijc'\
    '4NjI2NyIsImV4cCI6MTU5MTY3MTc0N30.XX3gz'\
        '5wyKxR4Lvapd4kl4bJBeaj0XSEr_Neb19PyGhA'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}
# Search code
payload = {
    "code": "17315643"
}
url = 'http://127.0.0.1:8000/api/v1/transaction/search/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
response.json()
print(response.json())

# {'amount': '1000.00',
#     'destination_content_object': {'address': 'Lome',
#                                    'country': None,
#                                    'first_name': 'Betty',
#                                    'identification_number': None,
#                                    'identification_type': None,
#                                    'issuer_country': None,
#                                    'last_name': 'Davis',
#                                    'phone_number': '213-633-1514'},
#     'destination_country': 'SN',
#     'source_content_object': {'address': 'Dakar',
#                               'country': None,
#                               'first_name': 'Denise',
#                               'identification_document_deleivery_date':
#  '2007-12-12',
#                               'identification_document_expiry_date':
#  '2022-12-12',
#                               'identification_number': 'EB012412312',
#                               'identification_type': 'PP',
#                               'issuer_country': 'TG',
#                               'last_name': 'Benoit',
#                               'phone_number': '716-759-2189'},
#     'source_country': 'SN'}
