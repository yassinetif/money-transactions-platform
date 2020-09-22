import requests
import json

# Agent Stat
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiY29kZSI6Ijk3NDYxOCIsImV4cCI6MTYwMjMyMDI3M30.DCFVZU_mO0N_7dinu6a-2ivyOP9R9f4Wr2vWMxoqXWk'
headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}

url = 'http://217.69.6.52/api/v1/transaction/agent/finance/situation/'
response = requests.post(url, headers=headers)
print(response)
print(response.json())
