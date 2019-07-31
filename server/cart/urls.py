from django.urls import path

from .views import (CartPageView,
                    CartOrderAfterCheckView,
                    FavoritesView,
                    LastSeenView)


app_name = 'cart'

urlpatterns = [
    path('', CartPageView.as_view(), name='order'),
    path('aftercheck/<str:uuid>/', CartOrderAfterCheckView.as_view(), name='aftercheck'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
    path('last-seen/', LastSeenView.as_view(), name='last-seen')
]


