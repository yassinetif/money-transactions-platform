
from apps.core.utils.http import post_simple_json_request
from apps.core.errors import CallPartnerApiException
from apps.shared.repository.shared_repository import SharedRepository

def send_otp_sms(to, text):
    try:
        headers = {'Accept': 'application/vnd.apisms.v1+json', 'Content-Type': 'application/json'}
        payload = {'user_key': 'LwCqHrp4WRDsyndLyFoFy4NrQT0K520FrIda5kq90YJ2N4llRT', 'secret_key': 'l3nkvgtH3vlJK0Ed2Ma5EX46jQWAFVJxWHB0hSVtFf3eRgfRLM'}
        login_response = post_simple_json_request('https://crm.paydunya.com/api/v1/auth/login', payload, headers)
        token = login_response.get('access_token')
        app_key = 'jvZF2UEjH6Vb61FoOLH8F8I2GH23kljgD2hGXBVSmebKHREEvo'
        url = 'https://crm.paydunya.com/api/v1/sms/send'
        headers = {'Accept': 'application/vnd.apisms.v1+json', 'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        sms_payload = {"send_sms_request": {"type": "application", "app_key": app_key, "sms": [{"from": "Monnamon", "to": to, "text": text}]}}
        r = post_simple_json_request(url, sms_payload, headers)
        result = r.get('code') == '00'
        SharedRepository.save_notification('SMS', text, to, result)

    except Exception as e:
        SharedRepository.save_notification('SMS', text, to, False)
        raise CallPartnerApiException(str(e), 'unable to send SMS to {}.Partner API error'.format(to))
