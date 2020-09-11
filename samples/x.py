import requests
import json


headers = {'Content-Type': 'application/json'}
url = 'http://127.0.0.1:5000/notifications/5e99c61ccb84ea5b85e10860/date_lecture'
payload = {}
response = requests.put(url)
print(response)
