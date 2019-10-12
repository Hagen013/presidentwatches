import zeep
from zeep import Settings

class Client(object):
    
    WSDL_URL = 'https://tracking.russianpost.ru/rtm34?wsdl'
    
    def __init__(self, login, password):
        self._login = login
        self._password = password
        self._settings = Settings(strict=False)
        self._client = zeep.Client(self.WSDL_URL, settings=self._settings)
        
    def get_operation_history(self, barcode):
        result = self._client.service.getOperationHistory(
            OperationHistoryRequest={'Barcode': barcode, 'MessageType': 0},
            AuthorizationHeader={'login': self._login, 'password': self._password}
        )
        return result
