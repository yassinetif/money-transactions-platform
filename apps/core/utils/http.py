import json
import requests


def post_simple_json_request(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers).json()
    return response
