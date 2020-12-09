import requests
import json

# Agent Stat
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiY29kZSI6Ijk3NDYxOCIsImV4cCI6MTYwODgzMjM1MX0.2q1etqH6UIXfs7gtUt5ZJ8KPlZvbe0pC9-yBLMT8ecA'
headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}

url = 'http://217.69.6.52/api/v1/transaction/agent/finance/situation/'
response = requests.post(url, headers=headers)
print(response)
print(response.json())
