import requests
import json
headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:8000/api/v1/entity/agent/login/'
data = {'username': 'a', 'password': 'semperFidelis@1989'}
response = requests.post(url, data=json.dumps(data), headers=headers)
print (response.json())
