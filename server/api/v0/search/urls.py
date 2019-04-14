from django.urls import path

from .views import FacetesApiView


app_name = 'api'

urlpatterns = [
    path('facetes/', FacetesApiView.as_view())
]


