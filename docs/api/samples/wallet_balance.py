import requests
import json

# Cash to Cash
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/customer/wallet/balance/'
payload = {
    "phone_number": "913296986",
}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response)
print(response.json())
