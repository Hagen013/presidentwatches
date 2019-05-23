from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.cart import Cart
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
        identifier = request.data['model']
        self.cart.add_offer(identifier)
        return Response(self.cart.data)


class CartItemDetailsApiView(BaseCartAPIView):

    def put(self, request, identifier):
        return Response({})

    def delete(self, request, identifier):
        self.cart.delete_offer(identifier)
        return Response(self.cart.data)


class CartItemQuantityApiView(BaseCartAPIView):

    def get(self, request, identifier, quantity):
        return Response({})

    def put(self, request, identifier, quantity):
        self.cart.update_quantity(identifier, quantity)
        return Response(self.cart.data)