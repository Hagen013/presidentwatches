from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.cart import Cart
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
        print(request.data)
        print('tsoy')
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
