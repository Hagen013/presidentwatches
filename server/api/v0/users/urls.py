from django.urls import path

from .views import (
    UserOrdersListApiView,
    UserOrderDetailsApiView,
    UserProfileApiView,
    SubsribesListView
)

app_name = 'api'


urlpatterns = [
    path('subscribes/', SubsribesListView.as_view(), name='subsribes'),
    path('<str:user_pk>/', UserProfileApiView.as_view(), name='profile'),
    path('<str:user_pk>/orders/', UserOrdersListApiView.as_view(), name='orders'),
    path('<str:user_pk>/orders/<str:order_pk>', UserOrderDetailsApiView.as_view(), name='order'),
]
