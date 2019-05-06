from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# from .serializers import (PointDeliverySerializer,
#                           CurierDeliverySerializer)

# from delivery.models import Delivery
from kladr.models import Kladr
from .controller import (DeliveryController,
                         MultiDeliveryController)


class OneProductDeliveryAPIView(APIView):

    def post(self, request):
        try:
            kladr_code = request.data['kladr']
        except KeyError:
            return Response(status=400, data="required kladr field")

        try:
            product = request.data['product']
        except KeyError:
            return Response(status=400, data="required product field")

        if not(isinstance(kladr_code, str) and isinstance(product, dict)):
            return Response(status=400, data="Invalid data type kladr or product")

        if (frozenset(('product_type', 'price', 'purchase_price', 'vendor')).issubset(product.keys()) and
           product['product_type'] != ''):
            try:
                d_ctrl = DeliveryController(kladr=kladr_code, **product)
                return Response(d_ctrl.get_devivery_data())
            except (TypeError, ValueError) as ex:
                return Response(status=400, data="Invalid parametrs")
        else:
            return Response({})


class ManyProductsDeliveryAPIView(APIView):

    def post(self, request):
        try:
            kladr_code = request.data['kladr']
        except KeyError:
            return Response(status=400, data="required kladr field")

        try:
            products = request.data['products']
        except KeyError:
            return Response(status=400, data="required products field")

        if not(isinstance(kladr_code, str) and
               (isinstance(products,  list) or isinstance(products,  tuple))):
            return Response(status=400, data="Invalid data type kladr or products")

        if all((isinstance(product,  dict) and
                frozenset(('product_type', 'price', 'purchase_price', 'vendor')).issubset(product.keys()) and
                product['product_type'] != '' for product in products)):
            # try:
            d_ctrl = MultiDeliveryController(kladr=kladr_code, products=products)
            return Response(d_ctrl.get_devivery_data())
            # except (TypeError, ValueError) as ex:
            #     return Response(status=400, data="Invalid parametrs")
        else:
            return Response({})
