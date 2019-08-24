import json
from itertools import chain
from collections import defaultdict
import requests

import django_filters
from django_filters import Filter
from django_filters.fields import Lookup

from django.conf import settings
from django.db.models import Max, Min
from django.views.generic import TemplateView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from core.viewmixins import DiggPaginatorViewMixin
from core.utils import custom_redirect
from cart.models import Promocode

from cart.last_seen import LastSeenController
from reviews.models import ReviewStatus

from .models import CategoryPage, ProductPage
from .models import Attribute, AttributeValue
from .models import CategoryNodeOutdatedUrl as OutdatedUrl


class ProductPageFilter(django_filters.FilterSet):

    price = django_filters.NumberFilter()
    price__gte = django_filters.NumberFilter(field_name='_price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='_price', lookup_expr='lte')
    rating_gte = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    is_in_store = django_filters.BooleanFilter(field_name='is_in_store')

    class Meta:
        model = ProductPage
        exclude = ['image', 'thumbnail', 'manual', 'certificate', 'summary', 'rating_overall']


class CategoryPageView(DiggPaginatorViewMixin, ListView):
    """
    Класс View для отображения страницы категории
    """
    template_name = "pages/category.html"
    context_object_name = "products"

    model = CategoryPage
    product_model = ProductPage
    filter_class = ProductPageFilter
    attribute_class = Attribute
    value_class = AttributeValue

    paginate_by = 24

    allowed_sorting_options = {'-price': ('-_price', 'id'),
                               'price': ('_price', 'id'),
                               '-scoring': ('-scoring', 'id'),
                               'sale_percentage': ('-sale_percentage', 'id'),
                               'created_at': ('created_at', 'id')
                              }
    default_sorting_option = ('-scoring', 'id')
    nonfilter_options = {"sort_by", "price__gte", "price__lte"}

    def get(self, request, slug, *args, **kwargs):
        querydict = request.GET.dict()
        page = querydict.get('page', None)
        if page == '1':
            querydict.pop('page')
            return custom_redirect(
                'shop:category',
                slug,
                **querydict
            )
        self.category = self.get_category(slug=slug)

        if self.category.slug != slug:
            return custom_redirect(
                'shop:category',
                self.category.slug,
                **request.GET.dict()
            )

        self.added_values = []

        querylength = len(request.GET.keys())
        if querylength > 0:
            self.exact_category = self.get_exact_category(request)
            if self.category.id != self.exact_category.id:
                redirect_queryparams = self.get_redirect_queryparams(self.exact_category)
                return custom_redirect(
                    'shop:category',
                    self.exact_category.slug,
                    **redirect_queryparams
                )
        return super(CategoryPageView, self).get(self, request, *args, **kwargs)

    def get_category(self, slug):
        try:
            return self.model.objects.get(
                slug=slug
            )
        except ObjectDoesNotExist:
            try:
                return OutdatedUrl.objects.get(
                    slug=slug
                ).node
            except ObjectDoesNotExist:
                raise Http404

    def get_exact_category(self, request, *args, **kwargs):
        added_values = set()
        removed_values = set()
        self.queryparams = request.GET.dict()
        self.attrs_set = set(map(lambda x: x["key"], self.attribute_class.objects.all().values("key")))

        fields = list(filter(lambda x: x in self.attrs_set, self.queryparams))
        removed_fields = list(filter(lambda x: x[1:] in self.attrs_set, self.queryparams))

        for field in fields:
            values = {int(x) for x in self.queryparams.pop(field).split(',')}
            added_values.update(values)
        for field in removed_fields:
            values = {int(x) for x in self.queryparams.pop(field).split(',')}
            removed_values.update(values)

        category_values = {x['id'] for x in self.category.attribute_values.all().values('id')}
        print('SEARCH VALUES')
        self.search_values = category_values.difference(removed_values).union(added_values)
        print(self.search_values)
        exact_nodes = self.model.objects.get_exact_node(tuple(self.search_values))

        try:
            exact_node = exact_nodes[0]
        except IndexError:
            exact_node = self.category.get_root()

        # Сохранение добавленных через GET-параметры значений для
        # дальнейшнего использования (оптимизация)
        self.added_values = self.value_class.objects.filter(id__in=added_values)
        return exact_node

    def get_redirect_queryparams(self, node):
        queryparams = defaultdict(list)
        values = node.attribute_values.values("id").all()
        values_set = {value["id"] for value in values}
        difference = self.search_values.difference(values_set)
        if len(difference) > 0:
            query_values = self.value_class.objects.filter(id__in=difference)
        else:
            query_values = []

        for value in query_values:
            queryparams[value.attribute.key].append(value.id)

        for key, value in self.queryparams.items():
            queryparams[key].append(value)

        return queryparams

    def get_filters(self, *args, **kwargs):
        return self.attribute_class.objects.filter(is_filter=True).order_by('order')

    def get_default_queryset(self, *args, **kwargs):
        fields = list(filter(lambda x: x in self.attrs_set, self.request.GET))
        queryparams = self.request.GET.dict()

        if len(fields) > 0:
            for key, values in queryparams.items():
                if key in self.attrs_set:
                    values = values.split(",")
                    values = list(map(lambda x: int(x), values))
                    queryparams[key] = values

            for value in self.category.attribute_values.all():
                key = value.attribute.key
                if key in queryparams.keys():
                    queryparams[key].append(value.id)
                else:
                    queryparams[key] = [value.id]

            qs = self.product_model.objects.filter(is_in_stock=True)
            for key, values in queryparams.items():
                if key in self.attrs_set:
                    qs = qs.filter(attribute_values__in=values)
        else:
            qs = self.category.products

        qs = qs.filter(is_in_stock=True)

        self.prices = {}
        self.prices = qs.aggregate(Min('_price'), Max('_price'))

        if self.prices['_price__min'] is None:
            self.prices['_price__min'] = 0

        if self.prices['_price__max'] is None:
            self.prices['_price__max'] = 10000

        self.prices['price__gte'] = self.request.GET.get('price__gte', self.prices['_price__min'])
        self.prices['price__lte'] = self.request.GET.get('price__lte', self.prices['_price__max'])

        qs = self.filter_class(
            self.request.GET,
            queryset=qs
        ).qs.distinct()

        return qs

    def get_queryset(self, *args, **kwargs):
        sorting_option = self.request.GET.get('sort_by')
        sort_by = self.allowed_sorting_options.get(
            sorting_option,
            self.default_sorting_option
        )
        self.sorting_option = sort_by[0]
        qs = self.get_default_queryset(*args, **kwargs).order_by(*sort_by)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryPageView, self).get_context_data(**kwargs)
        context['category'] = self.category

        context['sorting_option'] = self.sorting_option
        context['filters'] = self.get_filters()

        # Значения в тегах
        self.node_values = self.value_class.objects.filter(categories=self.category)
        node_values_json = list(map(lambda tag: {"key": tag.attribute.key, "id": tag.id}, self.node_values))
        node_values_json = json.dumps(node_values_json)
        tags = list(chain(self.node_values, self.added_values))
        tags = sorted(tags, key=lambda x: x.attribute.order)
        tags_json = list(map(lambda tag: {"key": tag.attribute.key, "id": tag.id}, tags))
        tags_json = json.dumps(tags_json)
        context['tags'] = tags
        context['tags_json'] = tags_json
        context['node_values_json'] = node_values_json

        # Цены
        context['price__min'] = self.prices['_price__min']
        context['price__max'] = self.prices['_price__max']
        context['price__lte'] = self.prices['price__lte']
        context['price__gte'] = self.prices['price__gte']
        context['rating_gte'] = self.request.GET.get('rating_gte', None)
        
        return context



class ProductPageView(TemplateView):
    
    template_name = 'pages/product.html'

    model = ProductPage
    instance_context_name = 'product'

    def get(self, request, slug, *args, **kwargs):
        self.instance = self.get_instance(slug)
        controller = LastSeenController(request)
        controller.push(self.instance)
        return super(ProductPageView, self).get(self, request, *args, **kwargs)

    def get_instance(self, slug):
        try:
            return self.model.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise Http404

    def get_delivery_data(self):
        url = settings.GEO_LOCATION_SERVICE_URL + 'api/delivery/one_product/'

        kladr = self.request.COOKIES.get(
            'city_code',
            settings.DEFAULT_KLADR_CODE
        )
        product = {
            'product_type': 'CUBE',
            'price': self.instance._price,
            'purchase_price': self.instance._purchase_price,
            'vendor': self.instance.brand
        }
        data = {
            'kladr': kladr,
            'product': product
        }
        try:
            response = requests.post(url, json=data)
            delivery_data = response.json()
        except:
            delivery_data = {}
        return delivery_data

    def fetch_promocode(self):
        qs = Promocode.objects.filter(brands__contains=self.instance.brand).order_by('sale_amount')
        if len(qs) > 0:
            return qs[0]
        else:
            return None

    def get_sale_notes(self):
        if self.instance.is_sale:
            return ''
        else:
            promocode = self.fetch_promocode()
            if promocode is not None:
                return 'Акция! Скидка {amount}% на эту модель {brand} по промокоду {promocode}'.format(
                    amount=promocode.sale_amount,
                    brand=self.instance.brand,
                    promocode=promocode.name
                )
            else:
                return ''

    def get_context_data(self, *args, **kwargs):
        context = super(ProductPageView, self).get_context_data(**kwargs)

        context[self.instance_context_name] = self.instance
        context['category'] = CategoryPage.objects.get_by_product(self.instance)

        # Reviews
        reviews = self.instance.reviews.filter(status=ReviewStatus.Approved)
        count = reviews.count()

        # Promocode stuff
        context['sale_notes'] = self.get_sale_notes()
        
        context['reviews'] = reviews
        context['reviews_count'] = count
        context['rating_overall'] = self.instance.rating_overall
        context['delivery_data'] = self.get_delivery_data()
        context['videos'] = self.instance.videos.all()

        context['images'] = self.instance.images.all().order_by('order')

        return context
