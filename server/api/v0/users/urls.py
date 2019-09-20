from django.urls import path

from .views import (
    UsersListApiView,
    UserOrdersListApiView,
    UserOrderDetailsApiView,
    UserProfileApiView,
    SubsribesListView,
    PasswordRenewAPIView
)

app_name = 'api'


urlpatterns = [
    path('', UsersListApiView.as_view(), name='list'),
    path('subscribes/', SubsribesListView.as_view(), name='subsribes'),
    path('passwordreset/', PasswordRenewAPIView.as_view(), name='password-reset'),
    path('<str:user_pk>/', UserProfileApiView.as_view(), name='profile'),
    path('<str:user_pk>/orders/', UserOrdersListApiView.as_view(), name='orders'),
    path('<str:user_pk>/orders/<str:order_pk>', UserOrderDetailsApiView.as_view(), name='order'),
]
