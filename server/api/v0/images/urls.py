from rest_framework_nested import routers

from django.urls import re_path, path, include

from .views import ProductImagesUploadView

app_name = 'api'


urlpatterns = [
    path('/products/<int:pk>/upload/', ProductImagesUploadView.as_view()),
]
