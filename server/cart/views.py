from django.views.generic import TemplateView


class CartPageView(TemplateView):

    template_name = 'pages/cart.html'


class CartOrderAfterCheckView(TemplateView):

    template_name = 'pages/aftercheck.html'