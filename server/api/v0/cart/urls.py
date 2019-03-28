from django.urls import path

from .views import CartItemsApiView


app_name = 'api'

urlpatterns = [
    path('items/', CartItemsApiView.as_view())
]