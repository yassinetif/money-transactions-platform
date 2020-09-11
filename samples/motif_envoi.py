import requests
import json
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/shared/motifenvoi/'
response = requests.post(url, headers=headers)
print(response.json())

# {
#     'code': 'Dakar',
#     'libelle': '086796',
# }
