from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings

from .views import (
    ProfileView,
    RegisterView,
    LoginView,
    UserAftercheckView,
    LogoutView
)


app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('aftercheck/', UserAftercheckView.as_view(), name='aftercheck')
]
