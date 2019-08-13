import codecs
import requests
from requests.exceptions import ConnectionError

from django.conf import settings


def invalid(s):
    return '%' in s


class GeoLocationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        city_code = request.COOKIES.get('city_code', None)
        city_name_encoded = request.COOKIES.get('city_name', None)

        if city_code is None or city_name_encoded is None:
            url = settings.GEO_LOCATION_SERVICE_URL + 'api/geo_ip/external'

            remote_addr = request.META.get('REMOTE_ADDR')
            x_real_ip = request.META.get('X-Real-IP')
            if x_real_ip is not None:
                params = {'remote_addr': x_real_ip}
            else:
                params = {'remote_addr': remote_addr}

            try:
                data = requests.get(url, params=params).json()
                city_code = data['city_code']
                city_name_ru = data['city_name']
                city_name_encoded = city_name_ru.encode('utf-8').hex()
                request.set_cookie('city_code', city_code)
                request.set_cookie('city_name', city_name_encoded)
            except:
                city_code = '7700000000000'
                city_name_ru = 'Москва'
                city_name_encoded = city_name_ru.encode('utf-8').hex()
                request.set_cookie('city_code', city_code)
                request.set_cookie('city_name', city_name_encoded)
        elif invalid(city_name_encoded):
            url = settings.GEO_LOCATION_SERVICE_URL + 'api/geo_ip/by-code/{code}'.format(
                code=city_code
            )
            data = requests.get(url).json()
            city_name_ru = data['kladr_name']
            city_name_encoded = city_name_ru.encode('utf-8').hex()
            request.set_cookie('city_code', city_code)
            request.set_cookie('city_name', city_name_encoded)
        else:
            try:
                city_name_ru = codecs.decode(city_name_encoded, 'hex').decode('utf-8')
            except:
                city_code = '7700000000000'
                city_name_ru = 'Москва'
                city_name_encoded = city_name_ru.encode('utf-8').hex()
                request.set_cookie('city_code', city_code)
                request.set_cookie('city_name', city_name_encoded)

        request.user.city_code = city_code
        request.user.city_name = city_name_ru
        request.location = {
            "name": city_name_ru,
            "code": city_code
        }

        return self.get_response(request)



