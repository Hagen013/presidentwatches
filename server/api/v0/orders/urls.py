from rest_framework_nested import routers

from django.urls import re_path, include

from .views import OrderViewSet


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'', OrderViewSet, base_name='orders')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
