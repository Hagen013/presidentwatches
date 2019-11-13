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
from users.serializers import UserSerializer, UserSubscribeSerializer, UserMarketingGroupSerializer
from users.models import UserSubscribe, UserMarketingGroup
from tasks.users import send_new_password
from tasks.marketing import notify_existing_user, notify_created_user

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
    permissions_class = permissions.IsAdminUser

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
    permissions_class = permissions.IsAdminUser

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


class PasswordRenewAPIView(APIView, ListViewMixin):

    permissions_class = permissions.AllowAny

    def get(self, request):
        return Response({})

    def post(self, request, *args, **kwargs):
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


class UserMarketingGroupListView(APIView, ListViewMixin):

    model = UserMarketingGroup
    pagination_class  = LimitOffsetPagination
    serializer_class = UserMarketingGroupSerializer
    permissions_class = permissions.IsAdminUser

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Response({})

    def put(self, request, *args, **kwargs):
        groups = request.data
        error = False
        base_sales = None

        for group in groups:
            if group['name'] == 'Зарегестрированные':
                base_sales = group['sales']

        for group in groups:
            try:
                instance = self.model.objects.get(id=group['id'])
            except ObjectDoesNotExist:
                instance = None
                error = True

            if instance is not None:
                sales = group['sales']

                for key, value in base_sales.items():
                    received_value = sales.get(key, None)
                    if received_value is None:
                        sales[key] = value
                    elif received_value < value:
                        sales[key] = value

                formated_sales = {}
                for key, value in sales.items():
                    if value > 0:
                        formated_sales[key] = round(value, 2)
                
                instance.sales = formated_sales
                instance.full_clean()
                instance.save()
        
        if not error:
            return Response(
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

class UserMarketingGroupDetailsView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({})

    def put(self, request, *args, **kwargs):
        return Response({})


class ClubPriceRegistrationApiView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        model = request.data.get('model', None)
        print(model)

        if email is not None:
            try:
                user = User.objects.get(
                    email=email
                )
            except ObjectDoesNotExist:
                user = None

            if user is not None:

                notify_existing_user(pk=user.id, model=model)

                return Response(
                    status=status.HTTP_200_OK
                )


            else:
                group = None
                try:
                    group = UserMarketingGroup.objects.get(
                        name='Зарегестрированные'
                    )
                except ObjectDoesNotExist:
                    pass

                password = User.objects.make_random_password()
                
                user = User(
                    username=email,
                    email=email,
                    marketing_group=group
                )
                user.set_password(password)
                
                try:
                    user.full_clean()
                    user.save()
                    notify_created_user.delay(pk=user.pk, model=model, password=password)
                    return Response(
                        status=status.HTTP_200_OK
                    )
                except:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST
                    )

        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
