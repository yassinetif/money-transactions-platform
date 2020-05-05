import requests
import json
headers = {'Content-Type': 'application/json'}

# Pay cash to cash transactions
payload = {
    "code": "18334046",
    "agent": {
        "code": "786267"
    },
    "type": "RETRAIT_CASH",
    "paid_amount": "15000",
    "destination_content_object": {
        "first_name": "Akpene",
        "last_name": "WONU",
        "phone_number": "90909333",
        "address": "Lome",
        "country": "TG",
        'issuer_country': 'TG',
        "identification_type": "PP",
        "identification_number": "34675AFZ4S43",
        "identification_document_deleivery_date": "2012-12-12",
        "identification_document_expiry_date": "2022-12-12"
    }
}
url = 'http://127.0.0.1:8000/api/v1/transaction/pay/'
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.json())
