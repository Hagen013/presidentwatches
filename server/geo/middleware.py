import requests
from requests.exceptions import ConnectionError

from django.conf import settings

from transliterate import translit


def invalid(s):
    return '%' in s


class GeoLocationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        city_code = request.COOKIES.get('city_code', None)
        city_name_lat = request.COOKIES.get('city_name', None)

        if city_code is None or city_name_lat is None:
            url = settings.GEO_LOCATION_SERVICE_URL + 'api/geo_ip/external'
            remote_addr = request.META.get('X-Real-IP')
            params = {'remote_addr': remote_addr}

            try:
                data = requests.get(url, params=params).json()
                city_code = data['kladr_code']
                city_name_ru = data['kladr_name']
                city_name_lat = translit(city_name_ru, 'ru', reversed=True)
                request.set_cookie('city_code', city_code)
                request.set_cookie('city_name', city_name_lat)
            except:
                city_code = '7700000000000'
                city_name_ru = 'Москва'
        elif invalid(city_name_lat):
            url = settings.GEO_LOCATION_SERVICE_URL + 'api/geo_ip/by-code/{code}'.format(
                code=city_code
            )
            data = requests.get(url).json()
            city_name_ru = data['kladr_name']
            city_name_lat = translit(city_name_ru, 'ru', reversed=True)
            request.set_cookie('city_code', city_code)
            request.set_cookie('city_name', city_name_lat)
        else:
            city_name_ru = translit(city_name_lat, 'ru')

        request.user.city_code = city_code
        request.user.city_name = city_name_ru
        request.location = {
            "name": city_name_ru,
            "code": city_code
        }

        return self.get_response(request)
