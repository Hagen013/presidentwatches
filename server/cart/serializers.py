from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework import serializers

from core.serializers import DynamicFieldsModelSerializer
from cart.models import Order, Promocode
from tasks.sms_notifications import sms_notify
from .cart import Cart


class OrderCreateSerializer():
    
    def __init__(self, data, request, cart=None):
        
        print(data)
        self._user = self.get_user(request)
        if cart is None:
            self._cart = self.get_cart(request)
        else:
            self._cart = cart
        self._location = self.get_location(request)
        self._customer = self.get_customer_data(data)
        self._delivery = self.get_delivery_data(data)
        self._payment = self.get_payment_data(data)
        self._cpa = self.get_cpa_data(data)
        self._store = self.get_store_data()
        self._sale = self.get_sale()
        self._total_price = self.get_total_price()
        
        self._client_notes = self.get_client_notes(data)
        self._source = self.get_source(data)
        
        self._instance = Order(
            cart=self._cart.data,
            user=self._user,
            location=self._location,
            customer=self._customer,
            delivery=self._delivery,
            payment=self._payment,
            cpa=self._cpa,
            store=self._store,
            source=self._source,
            client_notes=self._client_notes,
            sale=self._sale,
            total_price=self._total_price
        )
        self._instance.uuid = Order._generate_uuid()

        for i in range(100):
            self._instance.public_id = Order._generate_public_id()
            try:
                Order.objects.get(public_id=self._instance.public_id)
            except ObjectDoesNotExist:
                break
    
    def get_cart(self, request):
        return Cart(request)
    
    def get_location(self, request):
        return {
            'city': {
                'name': request.location['name'],
                'code': request.location['code']
            }
        }
    
    def get_customer_data(self, data):
        return data.get('customer')
    
    def get_user(self, request):
        user = request.user if request.user.is_authenticated else None
        return user
    
    def get_delivery_data(self, data):
        return data.get('delivery')

    def get_payment_data(self, data):
        return data.get('payment')
    
    def get_cpa_data(self, data):
        return data.get('cpa', {})
    
    def get_store_data(self):
        return {}

    def get_client_notes(self, data):
        return data.get('client_notes')

    def get_source(self, data):
        return data.get('source')

    def get_sale(self):
        promocode = self._cart.data.get('promocode')
        sale = self._cart.data.get('total_sale')
        return {
            'promocode': promocode,
            'amount': sale
        }

    def get_total_price(self):
        return self._cart.data['total_price'] + self._delivery['price']
    
    def validate(self):
        self._instance.full_clean()
    
    @property
    def is_valid(self):
        pass
    
    def save(self):
        self._cart.clear()
        self._instance.save()
        if not settings.DEBUG:
            sms_notify.delay(self._instance.public_id)
        return self._instance


class OrderSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Order
        fields = (
            'id',
            'public_id',
            'uuid',
            'state',
            'cart',
            'user',
            'location',
            'customer',
            'delivery',
            'payment',
            'tracking',
            'created_at',
            'modified_at',
            'client_notes',
            'total_price',
            'sale'
        )
        read_only_fields = (
            'id',
            'user',
            'public_id'
        )


class OrderPrivateSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Order
        fields = (
            'id',
            'public_id',
            'uuid',
            '_order',
            'state',
            'cart',
            'source',
            'user',
            'location',
            'customer',
            'delivery',
            'cpa',
            'payment',
            'tracking',
            'created_at',
            'modified_at',
            'client_notes',
            'manager_notes',
            'store',
            'total_price',
            'sale',
            'cpa'
        )
        read_only_fields = (
            'id',
            'user',
            'public_id'
        )


class PromocodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promocode
        fields = (
            'name',
            'description',
        )