from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('products/', include('api.v0.products.urls', namespace='products')),
]
