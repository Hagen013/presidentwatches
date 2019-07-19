from django.urls import path

from .views import UploadWarehouseApiView


app_name = 'api'

urlpatterns = [
    path('uploads/warehouse/', UploadWarehouseApiView.as_view()),
]
