from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from cart.cart import Cart
from cart.models import Order, Promocode
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


class ApplyPromocodeAPIView(BaseCartAPIView):

    """
    Возвращает корзину и с примененным промокодом
    """

    model = Promocode

    def get(self, request, *args, **kwargs):
        name = request.GET.get('name', '')
        if len(name) == 0:
            self.cart.reset_promocode()
            return Response(
                self.cart.data,
                status=status.HTTP_200_OK
            )
        else:
            try:
                instance = self.model.objects.get(
                    name=name
                )
            except ObjectDoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND
                )
            self.cart.apply_promocode(instance)
            return Response(
                self.cart.data,
                status=status.HTTP_200_OK
            )


class CartApiView(BaseCartAPIView):

    def delete(self, request):
        deleted = self.cart.data['items']
        self.cart.clear()
        return Response({
            'deleted': deleted,
            'cart': self.cart.data,
        })


class CartItemsApiView(BaseCartAPIView):

    def post(self, request):
        pk = request.data['pk']
        qnt = request.data.get('qnt', None)
        if qnt is not None:
            qnt = int(qnt)
            self.cart.add_offer(pk, quantity=qnt)
        else:
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
        deleted = self.cart.data['items'][pk]
        self.cart.delete_offer(pk)
        return Response({
            'deleted': deleted,
            'cart': self.cart.data
        })


class CartItemQuantityApiView(BaseCartAPIView):

    def get(self, request, pk, quantity):
        return Response({})

    def put(self, request, pk, quantity):
        changed = self.cart.data['items'][pk]
        qnt = int(changed['quantity'])
        changed['quantity'] = qnt
        self.cart.update_quantity(pk, quantity)
        return Response({
            'changed': changed,
            'quantity': qnt,
            'cart': self.cart.data
        })


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
        
        cpa = request.data.get('cpa', None)

        if cpa is not None:
            data['cpa'] = cpa
        
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
