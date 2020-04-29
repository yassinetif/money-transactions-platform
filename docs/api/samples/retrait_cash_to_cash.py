import requests
import json
headers = {'Content-Type': 'application/json'}

# Pay cash to cash transactions
payload = {'code': '561852312', 'agent': {'code': '786267'},
           'type': 'RETRAIT_CASH', 'paid_amount': '15000'}
url = 'http://127.0.0.1:8000/api/v1/transaction/pay/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
