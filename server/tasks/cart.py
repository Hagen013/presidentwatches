from config.celery import app

from django.core.exceptions import ObjectDoesNotExist

from cart.models import Promocode


@app.task
def serve_promocode(code):
    try:
        promocode = Promocode.objects.get(
            name=code
        )
    except ObjectDoesNotExist:
        promocode = None

    if promocode is not None:
        if promocode.has_limited_use:
            limit = promocode.limit - 1
            if limit <= 0:
                promocode.delete()