from django.urls import path

from .views import FacetesApiView, FacetesCountApiView


app_name = 'api'

urlpatterns = [
    path('facetes/', FacetesApiView.as_view()),
    path('facetes/<str:key>/count/', FacetesCountApiView.as_view())
]
