from django.urls import path

from .views import FacetesApiView, FacetesCountApiView, SearchApiView


app_name = 'api'

urlpatterns = [
    path('', SearchApiView.as_view()),
    path('facetes/', FacetesApiView.as_view()),
    path('facetes/<str:key>/count/', FacetesCountApiView.as_view())
]
