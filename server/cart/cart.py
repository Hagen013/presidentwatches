from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from shop.models import ProductPage


class Cart():

    CART_SESSION_ID = 'cart'

    def __init__(self, request):
        self.session = request.session
        data = self.session.get(self.CART_SESSION_ID)
        if not data:
            data = self.get_empty_data()
            self.session[self.CART_SESSION_ID] = data

        self.data = data
        self.ids = set(self.data['items'].keys())
        self.ids = {int(pk) for pk in self.ids}

    
    def add_offer(self, pk):
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
                now = datetime.now().isoformat()
                item = {
                    'pk': instance.id,
                    'model': instance.model,
                    'price': instance.price,
                    'quantity': 1,
                    'total_price': instance.price,
                    'image': instance.thumbnail.url,
                    'slug': instance.slug,
                    'url': instance.absolute_url,
                    'added_at': now,
                    'brand': instance.brand,
                    'series': instance.series
                }
                self.data['items'][pk] = item
                self.save()
        else:
            item['quantity'] += 1
            item['total_price'] = item['quantity'] * item['price']
            self.save()

    def add_offers(self, pks):
        qs = ProductPage.objects.filter(
            pk__in=pks
        )
        now = datetime.now().isoformat()
        for instance in qs:
            item = self.data['items'].get(instance.id, None)
            if item is None:
                item = {
                    'pk': instance.id,
                    'model': instance.model,
                    'price': instance.price,
                    'quantity': 1,
                    'total_price': instance.price,
                    'image': instance.thumbnail.url,
                    'slug': instance.slug,
                    'url': instance.absolute_url,
                    'added_at': now,
                    'brand': instance.brand,
                    'series': instance.series
                }
                self.data['items'][instance.pk] = item
            else:
                item['quantity'] += 1
                item['total_price'] = item['quantity'] * item['price']
        self.save()

    def delete_offer(self, offer_identifier):
        del self.data['items'][offer_identifier]
        self.save()

    def update_quantity(self, offer_identifier, quantity):
        item = self.data['items'][offer_identifier]
        item['quantity'] = quantity
        item['total_price'] = item['price'] * quantity
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

    def refresh_cart(self):
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

    def get_empty_data(self):
        now = datetime.now().isoformat()
        data = {
            'created_at': now,
            'modified_at': now,
            'items': {},
            'total_price': 0,
            'total_quantity': 0,
            'items_quantity': 0
        }
        return data

    @property
    def items_list(self):
        return list(self.data['items'].values())

    # Сохранение данных в сессию
    def save(self):
        self.refresh_cart()
        self.data['modified_at'] = datetime.now().isoformat()
        self.session[self.CART_SESSION_ID] = self.data
        self.session.modified = True

    # Очистка корзины
    def clear(self):
        data = self.get_empty_data()
        self.session[self.CART_SESSION_ID] = data
        self.data = data
