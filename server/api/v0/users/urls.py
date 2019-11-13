from django.urls import path

from .views import (
    UsersListApiView,
    UserOrdersListApiView,
    UserOrderDetailsApiView,
    UserProfileApiView,
    SubsribesListView,
    PasswordRenewAPIView,
    UserMarketingGroupListView,
    UserMarketingGroupDetailsView,
    ClubPriceRegistrationApiView
)

app_name = 'api'


urlpatterns = [
    path('', UsersListApiView.as_view(), name='list'),
    path('subscribes/', SubsribesListView.as_view(), name='subsribes'),
    path('passwordreset/', PasswordRenewAPIView.as_view(), name='password-reset'),
    path('club-prices/' , UserMarketingGroupListView.as_view(), name='club-prices'),
    path('get-club-price/', ClubPriceRegistrationApiView.as_view(), name='get-club-prices'),
    path('<str:user_pk>/', UserProfileApiView.as_view(), name='profile'),
    path('<str:user_pk>/orders/', UserOrdersListApiView.as_view(), name='orders'),
    path('<str:user_pk>/orders/<str:order_pk>', UserOrderDetailsApiView.as_view(), name='order'),
    #path('club-prices/<str:pk>/' , UserMarketingGroupDetailsView.as_view(), name='club-prices-details'),
]
