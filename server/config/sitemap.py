from django.urls import include, re_path, reverse

from django.contrib.sitemaps import GenericSitemap, Sitemap

from shop.models import ProductPage as Product
from shop.models import CategoryPage as Node


import datetime
from calendar import timegm
from functools import wraps

from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.http import http_date


def x_robots_tag(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner


@x_robots_tag
def sitemap_index(request, sitemaps,
          template_name='sitemap_index.xml', content_type='application/xml',
          sitemap_url_name='django.contrib.sitemaps.views.sitemap'):

    req_protocol = 'https'
    req_site = 'new.presidentwatches.ru'

    sites = []  # all sections' sitemap URLs
    for section, site in sitemaps.items():
        # For each section label, add links of all pages of its sitemap
        # (usually generated by the `sitemap` view).
        if callable(site):
            site = site()
        protocol = req_protocol if site.protocol is None else site.protocol
        sitemap_url = reverse(sitemap_url_name, kwargs={'section': section})
        absolute_url = '%s://%s%s' % (protocol, req_site, sitemap_url)
        sites.append(absolute_url)
        # Add links to all pages of the sitemap.
        for page in range(2, site.paginator.num_pages + 1):
            sites.append('%s?p=%s' % (absolute_url, page))

    return TemplateResponse(request, template_name, {'sitemaps': sites},
                            content_type=content_type)


@x_robots_tag
def sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

    req_protocol = 'https'
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = sitemaps.values()
    page = request.GET.get("p", 1)

    lastmod = None
    all_sites_lastmod = True
    urls = []
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
            if all_sites_lastmod:
                site_lastmod = getattr(site, 'latest_lastmod', None)
                if site_lastmod is not None:
                    site_lastmod = (
                        site_lastmod.utctimetuple() if isinstance(site_lastmod, datetime.datetime)
                        else site_lastmod.timetuple()
                    )
                    lastmod = site_lastmod if lastmod is None else max(lastmod, site_lastmod)
                else:
                    all_sites_lastmod = False
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    response = TemplateResponse(request, template_name, {'urlset': urls},
                                content_type=content_type)
    if all_sites_lastmod and lastmod is not None:
        # if lastmod is defined for all sites, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        response['Last-Modified'] = http_date(timegm(lastmod))
    return response


class DefaultSitemap(Sitemap):

    def get_urls(self, page=1, site=None, protocol='https'):
        # Determine protocol
        if self.protocol is not None:
            protocol = self.protocol
        if protocol is None:
            protocol = 'https'

        domain = 'new.presidentwatches.ru'

        if getattr(self, 'i18n', False):
            urls = []
            current_lang_code = translation.get_language()
            for lang_code, lang_name in settings.LANGUAGES:
                translation.activate(lang_code)
                urls += self._urls(page, protocol, domain)
            translation.activate(current_lang_code)
        else:
            urls = self._urls(page, protocol, domain)

        return urls


class CustomGenericSitemap(DefaultSitemap, GenericSitemap):
    pass


class StaticViewSitemap(DefaultSitemap):

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
    'categories': CustomGenericSitemap({
        'queryset': Node.objects.all(),
        'date_field': 'modified_at'
    }),
    'products': CustomGenericSitemap({
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