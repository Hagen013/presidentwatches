from django.conf.urls import url, include

from .views import (GeoIpAPIView,
                    GeoIpExternalRequestAPIView,
                    GeoIpByCode,
                    GeoIpCoordinatesAPIView)

geo_ip_urls = (
    [
        url(r'^$', GeoIpAPIView.as_view()),
        url(r'^external/$', GeoIpExternalRequestAPIView.as_view()),
        url(r'^by-code/(?P<code>(\d{13})|(\d{17})|(\d{19}))$', GeoIpByCode.as_view()),
        url(r'^coordinates/$', GeoIpCoordinatesAPIView.as_view()),
    ],
    'geo_ip'
)
