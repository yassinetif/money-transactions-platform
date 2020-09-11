import requests
import json

# Cash to Cash
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiY29kZSI'\
    '6IjA4Njc5NiIsImV4cCI6MTU5MTY3MTYwMX0.cG1OgCtGa4GOxa7_cuODR'\
        'kybMXVjop11o2siAFrceHY'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}
url = 'http://127.0.0.1:8000/api/v1/transaction/create/'
payload = {
    "type": "DEBIT_COMPTE_ENTITE",
    "account_number": "913296986",
    "amount": "5000",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response)
print(response.json())
