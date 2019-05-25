from django.urls import path

from .views import (CartApiView,
                    CartItemsApiView,
                    CartItemDetailsApiView,
                    CartItemQuantityApiView)


app_name = 'api'

urlpatterns = [
    path('', CartApiView.as_view()),
    path('items/', CartItemsApiView.as_view()),
    path('items/<str:pk>/', CartItemDetailsApiView.as_view()),
    path('items/<str:pk>/quantity/<int:quantity>/', CartItemQuantityApiView.as_view()),
]
