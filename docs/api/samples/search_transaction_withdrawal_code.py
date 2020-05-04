import requests
import json
headers = {'Content-Type': 'application/json'}

# Search code
payload = {
    "code": "WR14636702",
    "agent": {
        "code": "086796"
    }
}
url = 'http://127.0.0.1:8000/api/v1/transaction/search/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
response.json()
