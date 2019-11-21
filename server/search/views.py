from itertools import chain

from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from digg_paginator import DiggPaginator

from core.viewmixins import DiggPaginatorViewMixin
from config.es_client import es_client
from shop.models import ProductPage, CategoryPage
from .patterns import generate_from_pattern


class ElasticSearchQuery(object):

    def __init__(self, body, index, doc_type, es_client, page_size):
        self._body = body
        self._index = index
        self._doc_type = doc_type
        self._es_client = es_client
        self._page_size = page_size
        self._results = es_client.search(
            doc_type=self._doc_type,
            index=self._index,
            body=self._body
        )

    def __len__(self):
        return self._results['hits']['total']

    def __getitem__(self, key):
        self._body['from'] = key.start
        self._body['size'] = self._page_size
        results = es_client.search(
            doc_type=self._doc_type,
            index=self._index,
            body=self._body
        )
        return results['hits']['hits']


class ElasticsearchListView(TemplateView):

    query_kwarg = 'q'
    index = None
    doc_type = None

    paginator_class = DiggPaginator
    page_kwarg = 'page'
    paginate_by = 24
    paginate_orphans = 0
    paginate_allow_empty_first_page = True
    paginate_body = 5
    paginate_padding = 2
    paginate_margin = 2
    paginate_tail = 1

    product_model = ProductPage

    def get(self, request, *args, **kwargs):
        self.search_query = request.GET.get(self.query_kwarg, '')

        try:
            product = self.product_model.objects.get(
                model=self.search_query
            )
            return redirect('shop:product', slug=product.slug)
        except ObjectDoesNotExist:
            pass

        self.search_body = self.get_search_body()
        self.query = ElasticSearchQuery(
            self.search_body,
            self.index,
            self.doc_type,
            es_client,
            self.paginate_by
        )

        return super(ElasticsearchListView, self).get(request, *args, **kwargs)

    def get_search_body(self):
        raise NotImplementedError(
            'get_search_body method must be implemented by a subclass of ElastiListView'
        )

    def get_queryset(self, search_results):

        mapping = {}

        for result in search_results:
            identifier = result['_type']
            identifier += str(result['_source']['id'])
            mapping[identifier] = result['_score']
        
        # К этому моменту нам наплевать на Queryset evaluation, т.к.
        # мы уже получаем слайс на максимум -> page_size
        products = list(filter(lambda x: x['_type'] == 'product', search_results))
        categories = list(filter(lambda x: x['_type'] == 'category', search_results))

        products_ids = [product['_source']['id'] for product in products]
        categories_ids = [category['_source']['id'] for category in categories]

        qs_product = ProductPage.objects.filter(id__in=products_ids)
        qs_category = CategoryPage.objects.filter(id__in=categories_ids)

        qs = list(chain(qs_product, qs_category))
        
        # Здесь сделать сортировку по релевантности

        return qs

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        return self.paginator_class(
            queryset,
            per_page,
            orphans=self.paginate_orphans,
            allow_empty_first_page=self.paginate_allow_empty_first_page,
            body=self.paginate_body,
            padding=self.paginate_padding,
            margin=self.paginate_margin,
            tail=self.paginate_tail,
            **kwargs
        )

    def paginate_search(self, query, page_size):
        paginator = self.get_paginator(query, self.paginate_by)
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': force_text(e),
            })

    def get_context_data(self):
        paginator, page, search_results, is_paginated = self.paginate_search(self.query, self.paginate_by)
        qs = self.get_queryset(search_results)
        context = {
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            'results': qs,
            'query': self.search_query
        }
        return context


class SearchResultsView(ElasticsearchListView):

    template_name = 'pages/search.html'
    index = 'store'
    doc_type = 'category,product'

    def get_search_body(self):
        return generate_from_pattern(self.search_query)


class CustomSearchView(ElasticsearchListView):

    template_name = 'pages/search.html'
    index = 'store'
    doc_type = 'product'
    strict_mode = False

    def get_search_body(self):
        return generate_from_pattern(self.search_query)

    def get(self, request, *args, **kwargs):
        self.search_query = request.GET.get(self.query_kwarg, '')

        try:
            product = self.product_model.objects.get(
                model=self.search_query
            )
            return redirect('shop:product', slug=product.slug)
        except ObjectDoesNotExist:
            pass

        qs = self.product_model.objects.filter(
            model__istartswith=self.search_query
        )
        if qs.count() > 0:
            self.strict_mode = True
            self.qs = qs
        else:
            self.search_body = self.get_search_body()
            self.query = ElasticSearchQuery(
                self.search_body,
                self.index,
                self.doc_type,
                es_client,
                self.paginate_by
            )
        return super(ElasticsearchListView, self).get(request, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(ElasticsearchListView, self).get_context_data(*args, **kwargs)
        if not self.strict_mode:
            paginator, page, search_results, is_paginated = self.paginate_search(self.query, self.paginate_by)
            qs = self.get_queryset(search_results)

            context['paginator'] = paginator
            context['page_obj'] = page
            context['is_paginated'] = is_paginated
            context['results'] = qs
            context['query'] = self.search_query

            return context
        else:
            paginator = self.get_paginator(self.qs, per_page=24)
            page_kwarg = self.page_kwarg
            page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
            try:
                page_number = int(page)
            except ValueError:
                if page == 'last':
                    page_number = paginator.num_pages
                else:
                    raise Http404(_("Page is not 'last', nor can it be converted to an int."))
            try:
                page = paginator.page(page_number)
                # return (paginator, page, page.object_list, page.has_other_pages())
            except InvalidPage as e:
                raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                    'page_number': page_number,
                    'message': force_text(e),
                })
            

            context['paginator'] = paginator
            context['page_obj'] = page
            context['is_paginated'] = page.has_other_pages()
            context['results'] = page.object_list
            context['query'] = self.search_query

            return context



