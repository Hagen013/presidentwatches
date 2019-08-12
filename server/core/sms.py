import requests

from django.conf import settings

smsru_auth_sender = 'PWatches'


class SMSMessage():

    def __init__(self, phone, message, sender='PWatches'):
        self._phone = phone
        self._message = message
        self._sender = sender
        if secret_key is None:
            self._secret_key = settings.SMS_SECRET_KEY

    def send(self):
        payload = {
            "api_id": self._secret_key,
            "msg": self._message,
            "to": self._phone,
            "from": self._sender
        }
        response = requests.get(url=settings.SMS_URL, params=payload)
        return response