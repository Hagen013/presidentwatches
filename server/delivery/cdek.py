import requests
import datetime
from io import StringIO
from hashlib import md5
from urllib.parse import urlencode
from urllib.request import urlopen
from xml.etree.ElementTree import fromstring, ElementTree, Element, SubElement, tostring, ParseError


class Client(object):
    
    INTEGRATOR_URL = "https://integration.cdek.ru"
    ORDER_STATUS_URL = INTEGRATOR_URL + "/status_report_h.php"
    ORDER_INFO_URL = INTEGRATOR_URL + "/info_report.php"
    array_tags = {'State', 'Delay', 'Good', 'Fail', 'Item', 'Package', 'Order'}
    
    def __init__(self, login, password):
        self._login = login
        self._password = password
    
    @classmethod
    def _exec_request(cls, url, payload, method='GET'):
        if method == 'GET':
            pass
        elif method == 'POST':
            response = requests.post(url, data=payload)
        else:
            raise NotImplementedError('Unknown method "%s"' % method)
        return response
    
    @classmethod
    def _parse_xml(cls, data):
        try:
            xml = ElementTree(fromstring(data))
        except ParseError:
            pass
        else:
            return xml.getroot()
        
    @classmethod
    def _xml_to_dict(cls, xml):
        result = xml.attrib

        for child in xml.getchildren():
            if child.tag in cls.array_tags:
                result[child.tag] = result.get(child.tag, [])
                result[child.tag].append(cls._xml_to_dict(child))
            else:
                result[child.tag] = cls._xml_to_dict(child)

        return result
    
    def _xml_to_string(self, xml):
        return tostring(xml, method='xml')
        
    def _make_secure(self, date):
        raw = ('%s&%s' % (date, self._password)).encode()
        return md5(raw).hexdigest()

    def _exec_xml_request(self, url, xml_element):
        date = datetime.datetime.now().isoformat()
        xml_element.attrib['Date'] = date
        xml_element.attrib['Account'] = self._login
        xml_element.attrib['Secure'] = self._make_secure(date)
        text_request = self._xml_to_string(xml_element)
        payload = {
            'xml_request': text_request
        }
        response = self._exec_request(url, payload, method='POST')
        return self._parse_xml(response.text)
        
    def get_orders_statuses(self, orders, show_history=True):
        status_report_element = Element('StatusReport', ShowHistory=str(int(show_history)))
        for order in orders:
            order_number = str(order['public_id'])
            SubElement(
                status_report_element,
                'Order',
                Number=order_number,
            )
        xml = self._exec_xml_request(self.ORDER_STATUS_URL, status_report_element)
        return self._xml_to_dict(xml)

    def get_orders_information(self, orders):
        info_request = Element('InfoRequest')
        for order in orders:
            dispatch_number = order['delivery_status']['dispatch_number']
            if dispatch_number != "":
                SubElement(
                    info_request,
                    'Order',
                    DispatchNumber=str(dispatch_number)
                )
        xml = self._exec_xml_request(self.ORDER_INFO_URL, info_request)
        return self._xml_to_dict(xml)
