# from rest_framework.routers import DefaultRouter
# from .views import ProductPageViewSet

# app_name = 'api'

# router = DefaultRouter()

# router.register(r'', ProductPageViewSet, base_name='products')
# urlpatterns = router.urls
from rest_framework_nested import routers

from django.urls import re_path, include

from .views import ProductPageViewSet, ProductValuesViewSet


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'', ProductPageViewSet, base_name='products')

values_router = routers.NestedSimpleRouter(router, r'', lookup='product')
values_router.register(r'values', ProductValuesViewSet, base_name='values')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    re_path(r'^', include(values_router.urls))
]
