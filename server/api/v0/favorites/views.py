from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from favorites.controller import FavoritesController


class BaseFavoritesAPIView(APIView):

    def initial(self, request, *args, **kwargs):
        """
        Получение корзины до вызова любого обработчика
        """
        super(BaseFavoritesAPIView, self).initial(request, *args, **kwargs)
        self.controller = FavoritesController(request)


class FavoritesListAPIView(BaseFavoritesAPIView):

    def get(self, request):
        return Response({})

    def post(self, request):
        pk = request.data['pk']
        self.controller.add_offer(pk)
        return Response(self.controller.data)


class FavoritesItemAPIVIew(BaseFavoritesAPIView):

    def delete(self, request, pk):
        self.controller.delete_offer(pk)
        return Response(self.controller.data)
