from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('v0/', include('api.v0.urls', namespace='v0'))
]
