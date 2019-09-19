from django.urls import path

from .views import (PaymentsListAPIView,
                    PaymentsDetailsAPIView,
                    CreatePaymentAPIView,
                    PaymentsNotificationsAPIView)


app_name = 'api'

urlpatterns = [
    path('', PaymentsListAPIView.as_view(), name='list'),
    path('<int:pk>', PaymentsDetailsAPIView.as_view(), name='details'),
    path('create/', CreatePaymentAPIView.as_view(), name='create'),
    path('notifications/', PaymentsNotificationsAPIView.as_view(), name='notifications')
]
