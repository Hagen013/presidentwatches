from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from cart.cart import Cart
from cart.models import Order, Promocode, GiftSalesTable
from cart.serializers import OrderCreateSerializer, GiftSalesTableSerializer
from favorites.controller import FavoritesController
from shop.models import ProductPage
from tasks.marketing import send_gift_price, label_gift_prices

from django.contrib.auth import get_user_model

User = get_user_model()


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
            if request.user.is_authenticated:
                self.cart.add_offer(pk, quantity=qnt, group=request.user.marketing_group)
            else:
                self.cart.add_offer(pk, quantity=qnt)
        else:
            if request.user.is_authenticated:
                self.cart.add_offer(pk, group=request.user.marketing_group)
            else:
                self.cart.add_offer(pk)
        return Response(self.cart.data)


class CartItemsBulkyApiView(BaseCartAPIView):

    def post(self, request):
        pks = request.data.get('pks', None)
        if pks is not None:
            if request.user.is_authenticated:
                self.cart.add_offers(
                    pks=pks,
                    group=request.user.marketing_group
                )
            else:
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
        if request.user.is_authenticated:
            self.cart.add_offers(pks=pks, group=request.user.marketing_group)
        else:
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

        if request.user.is_authenticated:
            cart.add_offer(product['pk'], group=request.user.marketing_group)
        else:
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


class GiftSalesTableView(APIView):

    model = GiftSalesTable
    serializer_class = GiftSalesTableSerializer
    permissions = permissions.IsAdminUser

    def get(self, request, *args, **kwargs):
        instance = self.model.objects.first()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        instance = self.model.objects.first()
        serializer = self.serializer_class(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            label_gift_prices.delay()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class GiftPriceApiView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email', None)
        product_pk = data.get('product_pk', None)
        if email is not None and product_pk is not None:
            try:
                user = User.objects.get(
                    email=email
                )
            except ObjectDoesNotExist:
                password = User.objects.make_random_password()
                user = User(
                    username=email,
                    email=email,
                    password=password
                )
                user.save()
            send_gift_price.delay(user_pk=user.pk, product_pk=product_pk)
            return Response(status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )
