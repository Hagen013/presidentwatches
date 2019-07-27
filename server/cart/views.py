import requests
import json

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.conf import settings

from cart.models import Order
from cart.cart import Cart


class CartPageView(TemplateView):

    template_name = 'pages/cart.html'

    def get(self, request, *args, **kwargs):
        self.cart = Cart(request)
        return super(CartPageView, self).get(request, *args, **kwargs)

    @property
    def products(self):
        products = []
        items = self.cart.data['items']
        for key in items.keys():
            products.append({
                'price': items[key]['price'],
                'purchase_price': items[key]['price'],
                'vendor': items[key]['brand'],
                'product_type': 'CUBE'    
            })
        return products

    def get_delivery_data(self, products):
        url = settings.GEO_LOCATION_SERVICE_URL + 'api/delivery/meny_products/'
        kladr = self.request.COOKIES.get(
            'city_code',
            settings.DEFAULT_KLADR_CODE
        )
        data = {
            'kladr': kladr,
            'products': self.products
        }
        try:
            response = requests.post(url, json=data)
            delivery_data = response.json()
            keys = delivery_data.keys()
        except:
            delivery_data = {}
        return delivery_data

    def get_context_data(self, *args, **kwargs):
        context = super(CartPageView, self).get_context_data(*args, **kwargs)
        products = self.products
        delivery_data = self.get_delivery_data(products)
        context['delivery_data'] = delivery_data
        context['products'] = json.dumps(products)

        curier_is_available = False
        if delivery_data['curier'] is not None:
            curier_is_available = True
            price = int(delivery_data['curier']['price'])
        else:
            price = 0

        delivery_points_is_available = False
        if delivery_data['delivery_point'] is not None:
            delivery_points_is_available = True

        context['delivery_price'] = price
        context['total_price'] = price + self.cart.data['total_price']
        context['curier_is_available'] = curier_is_available
        context['delivery_points_is_available'] = delivery_points_is_available

        return context


class CartOrderAfterCheckView(TemplateView):

    template_name = 'pages/aftercheck.html'
    model = Order

    def get(self, request, uuid, *args, **kwargs):
        self.order = self.get_order(uuid)
        return super(CartOrderAfterCheckView, self).get(request, *args, **kwargs)

    def get_order(self, uuid):
        try:
            return self.model.objects.get(
                uuid=uuid
            )
        except ObjectDoesNotExist:
            raise Http404

    def get_context_data(self, *args, **kwargs):
        context = super(CartOrderAfterCheckView, self).get_context_data(*args, **kwargs)
        context['order'] = self.order
        return context
