from django.urls import path

from .views import SearchResultsView, CustomSearchView


app_name = 'search'

urlpatterns = [
    path('', CustomSearchView.as_view(), name='results'),
]

