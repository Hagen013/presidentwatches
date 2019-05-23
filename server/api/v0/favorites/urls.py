from django.urls import path

from .views import  FavoritesListAPIView


app_name = 'api'

urlpatterns = [
    path('', FavoritesListAPIView.as_view()),
]
