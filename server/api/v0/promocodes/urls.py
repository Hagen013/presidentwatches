from django.urls import path

from .views import SearchByNamePromocodeAPIView


app_name = 'api'

urlpatterns = [
    path('search/', SearchByNamePromocodeAPIView.as_view()),
]
