from rest_framework.routers import DefaultRouter
from .views import ProductPageViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'', ProductPageViewSet, base_name='products')
urlpatterns = router.urls
