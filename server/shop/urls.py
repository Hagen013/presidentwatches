from django.urls import path, re_path
from django.views.generic import TemplateView
from django.conf import settings

from .views import CategoryPageView


app_name = 'shop'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    re_path(r'^shop/(?P<slug>(($)|([-_\.\d\w/]+/$)))', CategoryPageView.as_view(), name='category')
]
