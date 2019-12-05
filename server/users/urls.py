from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings

from .views import (
    ProfileView,
    RegisterView,
    LoginView,
    UserAftercheckView,
    LogoutView,
    UserEmailVerificationView,
    UserPasswordConfirmationView,
    UserClubPriceExistingView,
    UserClubPriceCreatedView,
    UserMailingView,
    UserMailingRedirectView,
    UserTestView,
    GiftPriceRedirectView
)


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/#payments', ProfileView.as_view(), name='profile-payments'),
    path('aftercheck/<str:uuid>/', UserAftercheckView.as_view(), name='aftercheck'),
    path('verification/<str:uuid>/', UserEmailVerificationView.as_view(), name='verification'),
    path('password-reset/<str:uuid>/', UserPasswordConfirmationView.as_view(), name='password-reset'),
    path('club-price-сreated/<str:uuid>/', UserClubPriceCreatedView.as_view(), name='club-price-created'),
    path('club-price-existing/<str:uuid>/', UserClubPriceExistingView.as_view(), name='club-price-existing'),
    path('mailing/<str:uuid>/', UserMailingRedirectView.as_view(), name='mailing'),
    path('test/', UserTestView.as_view(), name='test'),
    path('gift-price/<str:uuid>/', GiftPriceRedirectView.as_view(), name='gift-price')
]