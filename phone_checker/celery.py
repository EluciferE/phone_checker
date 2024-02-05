import os
from logging.config import dictConfig

from celery import Celery
from celery.signals import setup_logging

from phone_checker.settings.logging_settings import LOGGING_CONF

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phone_checker.settings')

app = Celery('phone_checker')

app.config_from_object('django.conf:settings', namespace='CELERY')


@setup_logging.connect
def config_loggers(*_, **__):
    dictConfig(LOGGING_CONF)


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def debug_error_task():
    print('debug')
    raise ValueError('debug error task')
