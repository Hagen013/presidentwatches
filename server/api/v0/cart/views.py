from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from cart.cart import Cart
from cart.models import Order
from cart.serializers import OrderCreateSerializer
from favorites.controller import FavoritesController
from shop.models import ProductPage


class BaseCartAPIView(APIView):

    def initial(self, request, *args, **kwargs):
        """
        Получение корзины до вызова любого обработчика
        """
        super(BaseCartAPIView, self).initial(request, *args, **kwargs)
        self.cart = Cart(request)


class CartApiView(BaseCartAPIView):

    def delete(self, request):
        self.cart.clear()
        return Response(self.cart.data)


class CartItemsApiView(BaseCartAPIView):

    def post(self, request):
        pk = request.data['pk']
        self.cart.add_offer(pk)
        return Response(self.cart.data)


class CartItemsBulkyApiView(BaseCartAPIView):

    def post(self, request):
        pks = request.data.get('pks', None)
        if pks is not None:
            self.cart.add_offers(
                pks=pks
            )
            return Response(self.cart.data)
        else:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST
            )

class Fav2CartTransferApiView(BaseCartAPIView):
    # Remote-procedure-call View actually

    def get(self, request):
        favorites = FavoritesController(request)
        pks = list(favorites.ids)
        self.cart.add_offers(pks=pks)
        return Response(self.cart.data)
    

class CartItemDetailsApiView(BaseCartAPIView):

    def put(self, request, pk):
        return Response({})

    def delete(self, request, pk):
        self.cart.delete_offer(pk)
        return Response(self.cart.data)


class CartItemQuantityApiView(BaseCartAPIView):

    def get(self, request, pk, quantity):
        return Response({})

    def put(self, request, pk, quantity):
        self.cart.update_quantity(pk, quantity)
        return Response(self.cart.data)


class FastBuyApiView(BaseCartAPIView):

    def post(self, request, pk):
        
        product = request.data['product']

        cart = Cart()
        cart.add_offer(product['pk'])

        data = {
            'customer': {
                'email': '',
                'phone': request.data.get('phone'),
                'name': '',
                'address': ''
            },
            'delivery': {
                'type': 'not_selected',
                'price': 0,
                'pvz_code': 'None',
                'pvz_service': 'None',
                'pvz_address': ''
            },
            'payment': {
                'type': 'not_selected',
            },
            'client_notes': '',
            'source': 3
        }

        serializer = OrderCreateSerializer(data, request, cart=cart)

        try:
            serializer.validate()
        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=e.messages
            )


        instance = serializer.save()

        data = {
            'cart': instance.cart,
            'uuid': instance.uuid,
            'public_id': instance.public_id
        }
        return Response(data)


class CreateOrderAPIView(BaseCartAPIView):

    serializer_class = OrderCreateSerializer
    model_classs = Order

    def post(self, request):

        serializer = self.serializer_class(
            request.data,
            request
        )

        try:
            serializer.validate()
        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=e.messages
            )
    
        instance = serializer.save()
        data = {
            'cart': instance.cart,
            'uuid': instance.uuid,
            'public_id': instance.public_id
        }
        return Response(data)
