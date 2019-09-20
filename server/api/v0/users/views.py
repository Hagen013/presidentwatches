from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from api.views import ListViewMixin

from cart.models import Order
from cart.serializers import OrderSerializer
from users.serializers import UserSerializer, UserSubscribeSerializer
from users.models import UserSubscribe
from tasks.users import send_new_password

from django.contrib.auth import get_user_model

User = get_user_model()


class UsersListApiView(APIView, ListViewMixin):

    model             = User
    serializer_class  = UserSerializer
    permissions_class = permissions.IsAdminUser
    pagination_class  = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserOrdersListApiView(APIView):

    model_class = Order
    serializer_class = OrderSerializer

    def get(self, request, user_pk):
        qs = self.model_class.objects.filter(user__pk=user_pk)
        serializer = OrderSerializer(qs, many=True)
        return Response(serializer.data)


class UserOrderDetailsApiView(APIView):

    def get(self, request, user_pk, order_pk):
        return Response({
        })


class UserProfileApiView(APIView):
    
    model = User
    serializer_class = UserSerializer

    def get(self, request, user_pk):

        try:
            instance = self.model.objects.get(
                pk=user_pk
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404)

        serializer = self.serializer_class(instance)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, user_pk):

        serializer = self.serializer_class(data=request.data, instance=request.user)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SubsribesListView(APIView):

    model = UserSubscribe
    serializer_class = UserSubscribeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class PasswordRenewAPIView(APIView):

    permissions_class = permissions.AllowAny

    def get(self, request):
        return Response({})

    def post(self, request, *args, **kwargs):
        print('hoy')
        data = request.data
        email = data.get('email')
        user = self.get_user(email)
        password = User.objects.make_random_password()
        send_new_password.delay(user.id, password)
        return Response(
            status=status.HTTP_200_OK
        )

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise Http404
