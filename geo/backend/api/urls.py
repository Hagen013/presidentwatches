from django.conf.urls import url, include

from .delivery.urls import delivery_urls
from .geo_ip.urls import geo_ip_urls
from .kladr.urls import kladr_urls

urls_api = ([
    url(r'^delivery/', include(delivery_urls)),
    url(r'^geo_ip/', include(geo_ip_urls)),
    url(r'^kladr/', include(kladr_urls)),
], 'api')
