from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from django.views.generic import TemplateView

from api.urls import urls_api


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(urls_api)),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
