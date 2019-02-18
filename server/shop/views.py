import json

import django_filters
from django_filters import Filter
from django_filters.fields import Lookup

from django.views.generic import TemplateView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from core.viewmixins import DiggPaginatorViewMixin
from core.utils import custom_redirect

from .models import CategoryPage, ProductPage
from .models import Attribute, AttributeValue


class ProductPageFilter(django_filters.FilterSet):

    price = django_filters.NumberFilter()
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

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

    allowed_sorting_options = {'-price': ('-price', 'id'),
                               'price': ('price', 'id'),
                               '-scoring': ('-scoring', 'id')}
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
        exact_nodes = self.node_class.objects.get_exact_node(tuple(self.search_values))

        try:
            exact_node = exact_nodes[0]
        except IndexError:
            exact_node = self.category.get_root()
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

            qs = self.product_class.objects.filter(is_in_stock=True)
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
        sort_by = self.allowed_sorting_options.get(sorting_option, self.default_sorting_option)
        return self.get_default_queryset(*args, **kwargs).order_by(*sort_by)

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryPageView, self).get_context_data(**kwargs)
        context['category'] = self.category

        # Node values formating
        self.node_values = self.value_class.objects.filter(categories=self.category)
        node_values_set = {str(value.id) for value in self.node_values}
        node_values = list(map(lambda x: {"key": x.attribute.key, "id": x.id}, self.node_values))
        node_values = json.dumps(node_values)

        context['filters'] = self.get_filters()
        
        return context



class ProductPageView():
    pass