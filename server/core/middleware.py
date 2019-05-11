from types import MethodType

from django.utils.deprecation import MiddlewareMixin
from django.http import SimpleCookie


def _set_cookie(self, key, value='', max_age=None, expires=None, path='/',
        domain=None, secure=False):
    self._resp_cookies[key] = value
    self.COOKIES[key] = value
    if max_age is not None:
        self._resp_cookies[key]['max-age'] = max_age
    if expires is not None:
        self._resp_cookies[key]['expires'] = expires
    if path is not None:
        self._resp_cookies[key]['path'] = path
    if domain is not None:
        self._resp_cookies[key]['domain'] = domain
    if secure:
        self._resp_cookies[key]['secure'] = True


def _delete_cookie(self, key, path='/', domain=None):
    self.set_cookie(key, max_age=0, path=path, domain=domain,
                    expires='Thu, 01-Jan-1970 00:00:00 GMT')
    try:
        del self.COOKIES[key]
    except KeyError:
        pass


class RequestCookiesMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        request._resp_cookies = SimpleCookie()
        request.set_cookie = MethodType(_set_cookie, request)
        request.delete_cookie = MethodType(_delete_cookie, request)

    def process_response(self, request, response):
        if hasattr(request, '_resp_cookies') and request._resp_cookies:
            for k, v in request._resp_cookies.items():
                response.set_cookie(k, v)
        return response
