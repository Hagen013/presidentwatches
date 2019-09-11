from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.views.generic.base import RedirectView

from .sitemap import urlpatterns as sitemaps


urlpatterns = [
    path('', include('shop.urls', namespace='shop')),
    path('api/', include('api.urls', namespace='api')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('search/', include('search.urls', namespace='search')),
    path('info/', include('info.urls', namespace='info')),
    path('u/', include('users.urls', namespace='users')),
    path('vostok-chasy', RedirectView.as_view(url='/shop/watches/russian/vostok/', permanent=False)),
    path('mikhail-moskvin', RedirectView.as_view(url='/shop/watches/russian/mihail-moskvin/', permanent=False)),
    path('chasy-polet', RedirectView.as_view(url='/shop/watches/russian/polet/', permanent=False)),
    path('casio', RedirectView.as_view(url='/shop/watches/japan/casio/', permanent=False)),
    path('g-shock-chasy', RedirectView.as_view(url='/shop/watches/japan/casio/casio-g-shock/', permanent=False)),
    path('orient', RedirectView.as_view(url='/shop/watches/japan/orient/', permanent=False)),
    path('chasy-q-q', RedirectView.as_view(url='/shop/watches/japan/qq/', permanent=False)),
    path('timex', RedirectView.as_view(url='/shop/watches/american/timex/', permanent=False)),
    path('romanson', RedirectView.as_view(url='/shop/watches/other/romanson/', permanent=False)),
    path('muzhskie-chasy-naruchnye', RedirectView.as_view(url='/shop/watches/mens/', permanent=False)),
    path('zhenskie-chasy-naruchnye', RedirectView.as_view(url='/shop/watches/women/', permanent=False)),
    path('watch', RedirectView.as_view(url='/shop/watches/', permanent=False)),
    path('shvejcarskie-chasy', RedirectView.as_view(url='/shop/watches/swiss/', permanent=False)),
    path('rossijskie-chasy', RedirectView.as_view(url='/shop/watches/russian/', permanent=False)),
    path('yaponskie-chasy-naruchnye', RedirectView.as_view(url='/shop/watches/japan/', permanent=False)),
    path('nemeckie-chasy', RedirectView.as_view(url='/shop/watches/german/', permanent=False)),
    path('amerikanskie-chasy', RedirectView.as_view(url='/shop/watches/american/', permanent=False)),
    path('dizajnerskie-chasy', RedirectView.as_view(url='/shop/watches/fashion/', permanent=False)),
    path('404', TemplateView.as_view(template_name='404.html'))
]

urlpatterns += sitemaps

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
