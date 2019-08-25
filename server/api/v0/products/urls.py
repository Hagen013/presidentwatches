from rest_framework_nested import routers

from django.urls import re_path, path, include

from .views import (ProductPageViewSet,
                    ProductValuesViewSet,
                    ProductImagesAPIView,
                    ProductImageUploadView,
                    ProductImagesUploadView)


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'', ProductPageViewSet, base_name='products')

values_router = routers.NestedSimpleRouter(router, r'', lookup='product')
values_router.register(r'values', ProductValuesViewSet, base_name='values')

urlpatterns = [
    path('<int:product_pk>/images/', ProductImagesAPIView.as_view()),
    path('<int:pk>/image/', ProductImageUploadView.as_view()),
    path('<int:pk>/images/upload/', ProductImagesUploadView.as_view()),
    re_path(r'^', include(router.urls)),
    re_path(r'^', include(values_router.urls)),
]
