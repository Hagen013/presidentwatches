from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('products/', include('api.v0.products.urls', namespace='products')),
    path('eav/', include('api.v0.eav.urls', namespace='eav')),
    path('search/', include('api.v0.search.urls', namespace='search')),
    path('cart/', include('api.v0.cart.urls', namespace='cart'))
]
