from config.celery import app
from celery.schedules import crontab

from .test_task import test_task, periodic_task
from .sync_sdek import sync_sdek_points
from .sync_pick_point import sync_pick_point
from .sync_sdek_v2 import sync_sdek


app.add_periodic_task(
    crontab(
        minute="0",
        hour="0",
        day_of_week="1"
    ),
    sync_sdek.s(),
    name='sync_sdek',
)

app.add_periodic_task(
    crontab(
        minute="0",
        hour="0",
        day_of_week="2"
    ),
    sync_pick_point.s(),
    name='sync_pick_point',
)

app.add_periodic_task(
    crontab(
        minute="0",
        hour="0",
        day_of_week="3"
    ),
    sync_sdek_points.s(),
    name='sync_sdek_points',
)
