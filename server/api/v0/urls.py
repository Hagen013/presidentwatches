from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('products/', include('api.v0.products.urls', namespace='products')),
    path('eav/', include('api.v0.eav.urls', namespace='eav')),
    path('search/', include('api.v0.search.urls', namespace='search')),
    path('cart/', include('api.v0.cart.urls', namespace='cart')),
    path('favorites/', include('api.v0.favorites.urls', namespace='favorites')),
    path('orders/', include('api.v0.orders.urls', namespace='orders')),
    path('auth/', include('api.v0.auth.urls', namespace='auth')),
    path('jwt/', include('api.v0.jwt.urls', namespace='jwt')),
    path('tasks/', include('api.v0.tasks.urls', namespace='tasks'))
]
