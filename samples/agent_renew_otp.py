import requests

# Agent OTP
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI'\
    '6MiwiY29kZSI6IjY2NTQ5MyIsImV4cCI6MTU5MjY3NjQ'\
        '5OX0.fh_DohPr_AtyMheoLN8S_nssRu0GTC4VvQAJMqWQMWI'

headers = {'Content-Type': 'application/json',
           'Authorization': 'token {}'.format(token)}

url = 'http://127.0.0.1:8000/api/v1/entity/agent/login/otp/renew/'
response = requests.get(url, headers=headers)
print(response.json())
