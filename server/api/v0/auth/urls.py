from django.urls import path

from .views import SessionBasedLoginApiView

app_name = 'api'

urlpatterns = [
    path('login/', SessionBasedLoginApiView.as_view()),
]
