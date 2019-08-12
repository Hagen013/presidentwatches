from django.urls import path

from .views import (
    UploadWarehouseApiView,
    DonwloadWarehouseApiView,
    DownloadFileApiView,
    UserChangeEmailApiView,
    UserChangePhoneApiView
)


app_name = 'api'

urlpatterns = [
    # STAFF TASKS
    path('uploads/warehouse/', UploadWarehouseApiView.as_view()),
    path('warehouse/generate/', DonwloadWarehouseApiView.as_view()),
    path('warehouse/results/', DownloadFileApiView.as_view()),
    # RPC TASKS
    path('users/change/email/', UserChangeEmailApiView.as_view()),
    path('users/change/phone/', UserChangePhoneApiView.as_view())
]