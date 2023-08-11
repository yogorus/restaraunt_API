"""Things needed to set up our celery worker"""
from celery import Celery
from src.config import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_USERNAME

celery = Celery(
    'tasks',
    broker=f'amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}//',
    # include=["src.celery.tasks"],
)
celery.autodiscover_tasks(['src.celery.tasks'])


celery.conf.beat_schedule = {
    'track_xlsx_to_db every 15 seconds': {
        'task': 'src.celery.tasks.run_async_func',
        'schedule': 15,
    },
}


# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         15.0, track_xlsx_to_db.s(), name="track_xlsx_to_db every 15 seconds"
#     )
