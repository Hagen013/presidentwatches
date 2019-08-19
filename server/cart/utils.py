from .models import Promocode


def get_promocode_by_brand(brand):
    return Promocode.objects.filter(brands__in=self.brand).order_by(sale_amount)
