from config.celery import app


@app.task
def test_task():
    return 'test task worked'


@app.task
def periodic_task():
    return 42

# from celery.schedules import crontab

# app.add_periodic_task(
#     crontab(minute='*'),
#     periodic_task.s(),
#     name='sync_delivery',
# )
