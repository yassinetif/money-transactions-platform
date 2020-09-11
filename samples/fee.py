import requests
import json

headers = {'Content-Type': 'application/json'}
# Pay cash to cash transactions
payload = {
    "source_country": "GN",
    "type": "CASH_TO_CASH",
    "destination_country": "SN",
    "amount": "800000"
}
url = 'http://127.0.0.1:8000/api/v1/transaction/fee/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())

# {
#     "fee": "51775.000000000000",
#     "response_code": "000",
#     "tota_amount": "851775.000000000000"
# }
