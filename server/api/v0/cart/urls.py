from django.urls import path

from .views import (CartApiView,
                    CartItemsApiView,
                    CartItemDetailsApiView,
                    CartItemQuantityApiView,
                    CartItemsBulkyApiView,
                    Fav2CartTransferApiView,
                    FastBuyApiView,
                    CreateOrderAPIView,
                    ApplyPromocodeAPIView,
                    GiftSalesTableSerializer)


app_name = 'api'

urlpatterns = [
    path('', CartApiView.as_view()),
    path('bulk/items/', CartItemsBulkyApiView.as_view()),
    path('fav2cart/', Fav2CartTransferApiView.as_view()),
    path('items/', CartItemsApiView.as_view()),
    path('items/<str:pk>/', CartItemDetailsApiView.as_view()),
    path('items/<str:pk>/quantity/<int:quantity>/', CartItemQuantityApiView.as_view()),
    path('fast-buy/<str:pk>/', FastBuyApiView.as_view()),
    path('create-order/', CreateOrderAPIView.as_view()),
    path('promocode/', ApplyPromocodeAPIView.as_view()),
    path('gift-prices/', GiftSalesTableSerializer.as_view())
]
