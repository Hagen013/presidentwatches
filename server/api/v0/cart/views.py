from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from cart.cart import Cart
from cart.models import Order
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
        user = request.user if request.user.is_authenticated else None

        cart = Cart()
        cart.add_offer(product['pk'])

        order = Order(
            cart=cart.data,
            user=user
        )

        public_id = Order._generate_public_id()
        order.public_id = public_id
        order.uuid = Order._generate_uuid()

        try:
            order.full_clean()
        except ValidationError as e:
            print(e.messages)
            return Response(status=400, data=e.messages)
        order.save()

        data = {
            'cart': order.cart,
            'uuid': order.uuid,
            'public_id': order.public_id
        }
        return Response(data)

class CreateOrderAPIView(BaseCartAPIView):

    def post(self, request):
        cart = self.cart.data

        user = request.user if request.user.is_authenticated else None
        order = Order(
            cart=cart,
            user=user
        )
        public_id = Order._generate_public_id()
        order.public_id = public_id
        order.uuid = Order._generate_uuid()

        try:
            order.full_clean()
        except ValidationError as e:
            return Response(status=400, data=e.messages)

        self.cart.clear()
        order.save()

        data = {
            'cart': order.cart,
            'uuid': order.uuid,
            'public_id': order.public_id
        }
        return Response(data)
