import requests
import json
import functools


class Client(object):
    
    API_URL = 'https://e-solution.pickpoint.ru/api/'
    LOGIN_URL = API_URL + '/login'
    LOGOUT_URL = API_URL + '/logout'
    STATES_URL = API_URL + '/getstates'
    TRACK_URL = API_URL + '/tracksending'
    MULTIPLE_TRACKS_URL = API_URL + '/tracksendings'
    SENDING_INFO_URL = API_URL + '/sendinginfo'
    
    def __init__(self, login, password, session_id=None):
        self._login = login
        self._password = password
        self._session_id = session_id
            
    def _exec_request(self, url, payload, method='GET'):
        headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain',
                'Content-Encoding': 'utf-8'
        }
        if method == 'GET':
            response = requests.get(url, params=payload)
        elif method == 'POST':
            response = requests.post(url, data=json.dumps(payload), headers=headers)
        else:
            raise NotImplementedError('Unknown method "%s"' % method)
        return response
    
    def login(self):
        payload = {
            'Login': self._login,
            'Password': self._password
        }
        response = self._exec_request(self.LOGIN_URL, payload, method='POST')
        if response.status_code == 200:
            self._session_id = response.json()['SessionId']
        else:
            msg = 'Invalid login response'
            raise Exception(msg)
        return response
    
    def check_auth(self):
        if self._session_id is None:
            msg = 'Login required'
            raise Exception(msg)
    
    def get_states(self):
        payload = dict()
        response = self._exec_request(self.STATES_URL, payload)
        return response.json()
    
    def track_sending(self, public_code):
        self.check_auth()
        payload = {
            'SessionId': self._session_id,
            'SenderInvoiceNumber': str(public_code)
        }
        response = self._exec_request(self.TRACK_URL, payload, method='POST')
        return response

    def track_sendings(self, invoices):
        self.check_auth()
        payload = {
            'SessionId': self._session_id,
            'Invoices': invoices
        }
        response = self._exec_request(self.MULTIPLE_TRACKS_URL, payload, method='POST')
        return response
    
    def get_order_info(self, invoice_number):
        self.check_auth()
        payload = {
            'SessionId': self._session_id,
            'SenderInvoiceNumber': str(invoice_number),
        }
        response = self._exec_request(self.SENDING_INFO_URL, payload, method='POST')
        return response
    
    def logout(self):
        self.check_auth()
        payload = {
            'SessionId': self._session_id
        }
        response = self._exec_request(self.LOGOUT_URL, payload, method='POST')
        if response.status_code != 200:
            msg = 'Invalid logout response'
            raise Exception(msg)
        return response
