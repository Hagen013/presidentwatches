from django.urls import path

from .views import PaymentsListAPIView, PaymentsDetailsAPIView


app_name = 'api'

urlpatterns = [
    path('', PaymentsListAPIView.as_view(), name='list'),
    path('<int:pk>', PaymentsDetailsAPIView.as_view(), name='details')
]
