from celery import shared_task
from config.celery import app
from celery.decorators import periodic_task
from .synchronizers.sdek_synchronizer import SdekCourierSynchronizer, \
    SdekDeliveryPointSynchronizer
from .synchronizers.pickpoint_synchronizer import PickpointSynchronizer
from datetime import timedelta
from celery.schedules import crontab


@app.task
def sync_sdek_delivery_point():
    SdekDeliveryPointSynchronizer().sync()


@app.task
def sync_sdek_couriers_delivery():
    SdekCourierSynchronizer().sync()


@app.task
def sync_pickpoint_delivery():
    PickpointSynchronizer().sync()


@app.task
def sync_delivery():
    sync_sdek_delivery_point.delay()
    sync_sdek_couriers_delivery.delay()
    sync_pickpoint_delivery.delay()


app.add_periodic_task(
    crontab(minute=0,
            hour=0,
            day_of_week=2,
            ),
    sync_delivery.s(),
    name='sync_delivery',
)
