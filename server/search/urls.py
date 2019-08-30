from django.urls import path

from .views import SearchResultsView, CustomSearchView


app_name = 'search'

urlpatterns = [
    path('', SearchResultsView.as_view(), name='results'),
]

