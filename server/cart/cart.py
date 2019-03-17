from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from shop.models import ProductPage


class Cart():

    CART_SESSION_ID = 'cart'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(self.CART_SESSION_ID)
        if not cart:
            now = datetime.now().isoformat()
            cart = {
                'created_at': now,
                'modified_at': now,
                'items': {},
                'total_price': 0,
                'quantity': 0,
            }
            self.session[self.CART_SESSION_ID] = cart

        self.cart = cart

    
    def add_offer(self, offer_identifier):
        item = self.cart['items'].get('offer_identifier')
        # Проверка на наличе в корзине
        # если есть -> инкремент
        # если нет -> создание
        if not item:
            try:
                instance = ProductPage.objects.get(
                    model=offer_identifier
                )
            except ObjectDoesNotExist:
                instance = None
            if instance is not None:
                now = datetime.now().isoformat()
                item = {
                    'model': instance.model,
                    'price': instance.price,
                    'quantity': 1,
                    'total_price': instance.price,
                    'image': instance.thumbnail.url,
                    'slug': instance.slug,
                    'url': instance.absolute_url,
                    'added_at': now,
                    'brand': instance.brand
                }
                self.cart['items']['offer_identifier'] = item
                self.save()
        else:
            item['quantity'] += 1
            item['total_price'] = item['quanity'] * item['price']
            self.save()

    def delete_offer(self, offer_identifier):
        del self.cart['items'][offer_identifier]
        self.save()

    def update_quantity(self, offer_identifier, quanity):
        item = self.cart['items']['offer_identifier']
        item['quanity'] = quanity
        item['total_price'] = item['price'] * quanity
        self.save()

    def calculate_total_price(self):
        total_price = 0
        for item in self.cart['items'].values():
            total_price += item['total_price']
        return total_price

    def calculate_total_quantity(self):
        total_quantity = 0
        for item in self.cart['items'].values():
            total_quantity += item['quantity']
        return total_quantity
    
    def calculate_items_quantity(self):
        return len(self.cart['items'])

    def refresh_cart(self):
        total_quantity = 0
        total_price = 0
        items_quantity = 0

        for item in self.cart['items'].values():
            total_price += item['total_price']
            total_quantity += item['quantity']
            items_quantity += 1

        self.cart['total_quantity'] = total_quantity
        self.cart['total_price'] = total_price
        self.cart['items_quantity'] = items_quantity

    # Сохранение данных в сессию
    def save(self):
        self.refresh_cart()
        self.cart['modified_at'] = datetime.now().isoformat()
        self.session(self.CART_SESSION_ID) = self.cart
        self.session.modified = True

    # Очистка корзины
    def clear(self):
        del self.session[self.CART_SESSION_ID]
        self.session.modified = True
