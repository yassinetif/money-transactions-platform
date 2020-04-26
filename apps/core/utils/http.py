import rstr
import json
import requests


def post_json_request(data):
    headers = {'Content-Type': 'application/json'}
    url = '127.0.0.1:8000/'
    response = requests.post(url, data=json.dumps(data), headers=headers).json()
    return response

