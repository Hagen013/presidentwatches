from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from shop.models import ProductPage
from .models import Promocode


class CartItemSerializer():

    def __init__(self, instance, date=None):
        self._instance = instance
        self._date = date

    @property
    def data(self):
        if self._date is None:
            self._date = datetime.now().isoformat()
        return {
            'pk': self._instance.id,
            'model': self._instance.model,
            'price': self._instance.price,
            'quantity': 1,
            'total_price': self._instance.price,
            'base_price': self._instance.price,
            'image': self._instance.thumbnail.url,
            'slug': self._instance.slug,
            'url': self._instance.absolute_url,
            'added_at': self._date,
            'brand': self._instance.brand,
            'series': self._instance.series,
            'is_sale': self._instance.is_sale,
            'sale': 0
        }


class Cart():

    CART_SESSION_ID = 'cart'

    def __init__(self, request=None):
        if request is not None:
            self.session = request.session
            self.user = request.user
            data = self.session.get(self.CART_SESSION_ID)
            if not data:
                data = self.get_empty_data()
                self.session[self.CART_SESSION_ID] = data
        else:
            self.user = None
            data = self.get_empty_data()
            self.CART_SESSION_ID = None

        self.data = data
        self.ids = set(self.data['items'].keys())
        self.ids = {int(pk) for pk in self.ids}

    
    def add_offer(self, pk, quantity=1, group=None):
        pk = str(pk)
        item = self.data['items'].get(pk)
        # Проверка на наличе в корзине
        # если есть -> инкремент
        # если нет -> создание
        if not item:
            try:
                instance = ProductPage.objects.get(
                    pk=pk
                )
            except ObjectDoesNotExist:
                instance = None
            if instance is not None:
                item = CartItemSerializer(instance).data
                item['quantity'] = quantity
                self.data['items'][pk] = item
                self.save()
        else:
            item['quantity'] += quantity
            item['total_price'] = item['quantity'] * item['price']
            item['base_price'] = item['total_price']
            self.save()

    def add_offers(self, pks, group=None):
        qs = ProductPage.objects.filter(
            pk__in=pks
        )
        now = datetime.now().isoformat()
        for instance in qs:
            item = self.data['items'].get(instance.id, None)
            if item is None:
                item = CartItemSerializer(instance).data
                self.data['items'][instance.pk] = item
            else:
                item['quantity'] += 1
                item['total_price'] = item['quantity'] * item['price']
                item['base_price'] = item['total_price']
        self.save()

    def delete_offer(self, offer_identifier):
        try:
            del self.data['items'][offer_identifier]
        except KeyError:
            pass
        self.save()

    def update_quantity(self, offer_identifier, quantity):
        item = self.data['items'][offer_identifier]
        item['quantity'] = quantity
        item['total_price'] = item['price'] * quantity
        item['base_price'] = item['total_price']
        self.save()

    def calculate_total_price(self):
        total_price = 0
        for item in self.data['items'].values():
            total_price += item['total_price']
        return total_price

    def calculate_total_quantity(self):
        total_quantity = 0
        for item in self.data['items'].values():
            total_quantity += item['quantity']
        return total_quantity
    
    def calculate_items_quantity(self):
        return len(self.data['items'])

    def recalculate(self):

        total_quantity = 0
        total_price = 0
        items_quantity = 0

        for item in self.data['items'].values():
            total_price += item['total_price']
            total_quantity += item['quantity']
            items_quantity += 1

        self.data['total_quantity'] = total_quantity
        self.data['total_price'] = total_price
        self.data['items_quantity'] = items_quantity

        promocode = self.data.get('promocode', None)
        if promocode is not None and len(promocode) > 0:
            try:
                promocode = Promocode.objects.get(
                    name=promocode
                )
            except ObjectDoesNotExist:
                promocode = None

            if promocode is not None:
                self.data = promocode.apply(self.data, self.user)


    def apply_promocode(self, promocode):
        self.data = promocode.apply(self.data, self.user)
        self.save_session()

    def reset_promocode(self):
        self.data['promocode'] = ''
        self.data['total_sale'] = 0

        for item in self.data['items'].values():
            item['total_price'] = item['price'] * item['quantity']

        self.recalculate()
        self.save_session()

    def get_empty_data(self):
        now = datetime.now().isoformat()
        data = {
            'created_at': now,
            'modified_at': now,
            'items': {},
            'total_price': 0,
            'total_quantity': 0,
            'items_quantity': 0,
            'total_sale': 0,
            'promocode': ''
        }
        return data

    # Сохранение данных в сессию
    def save(self):
        self.recalculate()
        self.save_session()

    def save_session(self):
        if self.CART_SESSION_ID is not None:
            self.session[self.CART_SESSION_ID] = self.data
            self.session.modified = True

    # Очистка корзины
    def clear(self):
        data = self.get_empty_data()
        if self.CART_SESSION_ID:
            self.session[self.CART_SESSION_ID] = data
        self.data = data

    @property
    def items_list(self):
        return sorted(list(self.data['items'].values()), key=lambda x: x['added_at'])

    @property
    def has_promocode(self):
        return self.data['total_sale'] > 0