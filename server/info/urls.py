from django.urls import path
from django.views.generic import TemplateView

app_name = 'info'

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='pages/info/about.html'), name='about'),
    path('contacts/', TemplateView.as_view(template_name='pages/info/about.html'), name='contacts'),
    path('delivery/', TemplateView.as_view(template_name='pages/info/delivery-and-payment.html'), name='delivery'),
    path('guarantees/', TemplateView.as_view(template_name='pages/info/guarantees.html'), name='guarantees'),
    path('privacy-policy/', TemplateView.as_view(template_name='pages/info/privacy-policy.html'), name='privacy'),
    path('oferta/', TemplateView.as_view(template_name='pages/info/oferta.html'), name='oferta'),
    path('promo/', TemplateView.as_view(template_name='pages/info/promo.html'), name='promo'),
]
