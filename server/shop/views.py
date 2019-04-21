import json
from itertools import chain
from collections import defaultdict

import django_filters
from django_filters import Filter
from django_filters.fields import Lookup

from django.db.models import Max, Min
from django.views.generic import TemplateView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from core.viewmixins import DiggPaginatorViewMixin
from core.utils import custom_redirect

from cart.last_seen import LastSeenController

from .models import CategoryPage, ProductPage
from .models import Attribute, AttributeValue


class ProductPageFilter(django_filters.FilterSet):

    price = django_filters.NumberFilter()
    price__gte = django_filters.NumberFilter(field_name='_price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='_price', lookup_expr='lte')

    class Meta:
        model = ProductPage
        exclude = ['image', 'thumbnail', 'manual', 'certificate']


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
                               'sale_percentage': ('sale_percentage', 'id'),
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
                url,
                querydict
            )
        self.category = self.get_category(slug=slug)

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
        self.search_values = category_values.difference(removed_values).union(added_values)
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

        qs = self.filter_class(
            self.request.GET,
            queryset=qs
        ).qs

        return qs.distinct()

    def get_queryset(self, *args, **kwargs):
        sorting_option = self.request.GET.get('sort_by')
        sort_by = self.allowed_sorting_options.get(
            sorting_option,
            self.default_sorting_option
        )
        self.sorting_option = sort_by[0]
        return self.get_default_queryset(*args, **kwargs).order_by(*sort_by)

    def get_prices(self, qs):
        prices = qs.aggregate(Min('_price'), Max('_price'))
        prices['price__gte'] = self.request.GET.get('price__gte', None)
        prices['price__lte'] = self.request.GET.get('price__lte', None)
        print(prices)
        return prices

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
        context['prices'] = self.get_prices(context['products'])

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

    def get_context_data(self, *args, **kwargs):
        context = super(ProductPageView, self).get_context_data(**kwargs)

        context[self.instance_context_name] = self.instance
        context['images'] = self.instance.images.all()

        return context
