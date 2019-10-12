from datetime import datetime, timedelta

from django.conf import settings
from django.db import transaction
from django.utils.timezone import now, pytz

from config.celery import app
from celery.schedules import crontab

from cart.models import Order
from delivery.cdek import Client as ClientSDEK
from delivery.pickpoint import Client as ClientPickpoint
from delivery.rupost import Client as ClientRupost
from cart.serializers import OrderSerializer
from cart.utils import (pickpoint_to_cdek_code,
                        rupost_to_cdek_code,
                        rupost_msg_to_code)


@app.task
def sync_sdek_orders(pks):

    errors = []
    invalid = []

    qs = Order.objects.filter(public_id__in=pks)

    return None


@app.task
def sync_pickpoint_orders(pks):
    return None


@app.task
def sync_postal_orders(pks):
    return None