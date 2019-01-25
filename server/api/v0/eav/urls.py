from rest_framework.routers import DefaultRouter
from .views import AttributeViewSet, AttributeGroupViewSet, AttributeValueViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'attributes', AttributeViewSet, base_name='attributes')
router.register(r'groups', AttributeGroupViewSet, base_name='groups')
router.register(r'values', AttributeValueViewSet, base_name='values')

urlpatterns = router.urls
