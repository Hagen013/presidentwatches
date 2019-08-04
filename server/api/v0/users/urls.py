from django.urls import path

from .views import (
    UserOrdersListApiView,
    UserOrderDetailsApiView,
    UserProfileApiView
)

app_name = 'api'


urlpatterns = [
    path('<str:user_pk>/', UserProfileApiView.as_view()),
    path('<str:user_pk>/orders/', UserOrdersListApiView.as_view()),
    path('<str:user_pk>/orders/<str:order_pk>', UserOrderDetailsApiView.as_view()),
]
