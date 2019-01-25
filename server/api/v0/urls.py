from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('products/', include('api.v0.products.urls', namespace='products')),
    path('eav/', include('api.v0.eav.urls', namespace='eav'))
]
