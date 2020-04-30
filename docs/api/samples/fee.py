import requests
import json
headers = {'Content-Type': 'application/json'}

# Pay cash to cash transactions
payload = {'source_country': 'SN', 'agent': {'code': '786267'},
           'type': 'CASH_TO_CASH', 'destination_country': 'SN', 'amount': '15000'}
url = 'http://127.0.0.1:8000/api/v1/transaction/fee/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
