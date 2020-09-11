import requests
import json

# Wallet Balance
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJp'\
    'ZCI6MiwiY29kZSI6Ijc4ODY1NTQzNCIsImV4cCI6'\
    'MTU5MjY4MDI5MX0.AMulkYCwcOkpvqLEnRUW0'\
    'EST4VJnqRfSLaKGlrdWm7w'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}
url = 'http://127.0.0.1:8000/api/v1/customer/wallet/balance/'
payload = {
    "phone_number": "788655434",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response)
print(response.json())

# <Response [200]>

# {'agent':
#  {'code': '665493',
#   'entity':
#   {'brand_name': 'KBS'
#    }, 'first_name': 'Test',
#   'last_name': 'User',
#   'username': 'test.user'},
#  'amount': '1000',
#     'date': '2020-06-28T17:45:21.876593',
#  'destination_content_object': {
#      'address': 'Lome',
#      'first_name': 'Betty',
#      'last_name': 'Davis',
#       'phone_number': '213-633-1514'
#  }, 'destination_country': 'SN',
#  'fee': '65.00',
#  'motif_envoi': 'salaire',
#  'paid_amount': '1065.00',
#  'receipt_code': '672433048',
#     'response_code': '000',
#  'source_content_object': {
#      'address': 'Dakar',
#      'first_name': 'Denise',
#       'identification_document_delivery_date': '2007-12-12',
#      'identification_document_expiry_date': '2022-12-12',
#      'identification_number': 'EB012412312',
#      'identification_type': 'PP',
#       'issuer_country': 'TG',
#      'last_name': 'Benoit',
#      'phone_number': '716-759-2189'
#  }, 'source_country': 'SN',
#  'source_revenu': 'salaire',
#  'transaction_number': '5422487362',
#  'type': 'CASH_TO_CASH'
#  }
