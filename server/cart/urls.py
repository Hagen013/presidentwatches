from django.urls import path

from .views import CartPageView, CartOrderAfterCheckView


app_name = 'cart'

urlpatterns = [
    path('', CartPageView.as_view(), name='order'),
    path('aftercheck/', CartOrderAfterCheckView.as_view(), name='aftercheck')
]


