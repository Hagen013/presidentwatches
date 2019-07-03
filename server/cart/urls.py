from django.urls import path

from .views import CartPageView, CartOrderAfterCheckView


app_name = 'cart'

urlpatterns = [
    path('', CartPageView.as_view(), name='order'),
    path('aftercheck/<str:uuid>/', CartOrderAfterCheckView.as_view(), name='aftercheck')
]


