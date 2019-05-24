from django.urls import path

from .views import  FavoritesListAPIView, FavoritesItemAPIVIew


app_name = 'api'

urlpatterns = [
    path('', FavoritesListAPIView.as_view()),
    path('items/<str:pk>/', FavoritesItemAPIVIew.as_view()),
]
