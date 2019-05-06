from django.conf.urls import url, include

from .views import GeoIpAPIView

geo_ip_urls = (
    [
        url(r'^$',
            GeoIpAPIView.as_view()
            ),
    ],
    'geo_ip'
)
