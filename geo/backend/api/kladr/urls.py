from django.conf.urls import url, include

from .views import (DetalKladrAPIView,
                    SearchKladrAPIView)

kladr_urls = (
    [
        url(r'^detal/$',
            DetalKladrAPIView.as_view()
            ),
        url(r'^detal/(?P<code>(\d{13})|(\d{17})|(\d{19}))$',
            DetalKladrAPIView.as_view()
            ),
        url(r'^search/(?P<line>(\w+))$',
            SearchKladrAPIView.as_view()
            )
    ],
    'kladr'
)
