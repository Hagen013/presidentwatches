from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from cart.models import Order


class CartPageView(TemplateView):

    template_name = 'pages/cart.html'


class CartOrderAfterCheckView(TemplateView):

    template_name = 'pages/aftercheck.html'
    model = Order

    def get(self, request, uuid, *args, **kwargs):
        self.order = self.get_order(uuid)
        return super(CartOrderAfterCheckView, self).get(request, *args, **kwargs)

    def get_order(self, uuid):
        try:
            return self.model.objects.get(
                uuid=uuid
            )
        except ObjectDoesNotExist:
            raise Http404

    def get_context_data(self, *args, **kwargs):
        context = super(CartOrderAfterCheckView, self).get_context_data(*args, **kwargs)
        context['order'] = self.order
        return context
