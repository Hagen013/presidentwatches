from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings

from .sitemap import urlpatterns as sitemaps


urlpatterns = [
    path('', include('shop.urls', namespace='shop')),
    path('api/', include('api.urls', namespace='api')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('search/', include('search.urls', namespace='search')),
    path('info/', include('info.urls', namespace='info')),
    path('u/', include('users.urls', namespace='users')),
]

urlpatterns += sitemaps

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
