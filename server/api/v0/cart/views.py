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


class CartItemsApiView(BaseCartAPIView):

    def post(self, request):
        identifier = request.data['model']
        self.cart.add_offer(identifier)
        print(self.cart.data)
        return Response(self.cart.data)