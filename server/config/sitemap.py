from django.urls import include, re_path, reverse

from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.contrib.sitemaps.views import sitemap, index as sitemap_index

from shop.models import ProductPage as Product
from shop.models import CategoryPage as Node


class StaticViewSitemap(Sitemap):

    def items(self):
        return [
            'info:about',
            'info:contacts',
            'info:delivery',
            'info:guarantees',
            'info:privacy',
            'info:oferta',
            'info:shops',
        ]

    def location(self, item):
        return reverse(item)


sitemaps = {
    'categories': GenericSitemap({
        'queryset': Node.objects.all(),
        'date_field': 'modified_at'
    }),
    'products': GenericSitemap({
        'queryset': Product.objects.all(),
        'date_field': 'modified_at'
    }),
    "static-pages": StaticViewSitemap
}


urlpatterns = [
    re_path(r'^sitemap', include([
        re_path(r'^\.xml$', sitemap_index, {"sitemaps": sitemaps}),
        re_path(r'^-(?P<section>.+)\.xml$', sitemap, {
            "sitemaps": sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
        ])),
]