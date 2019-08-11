from django.urls import path

from .views import (
    UploadWarehouseApiView,
    DonwloadWarehouseApiView,
    DownloadFileApiView
)


app_name = 'api'

urlpatterns = [
    path('uploads/warehouse/', UploadWarehouseApiView.as_view()),
    path('warehouse/generate/', DonwloadWarehouseApiView.as_view()),
    path('warehouse/results/', DownloadFileApiView.as_view())
]