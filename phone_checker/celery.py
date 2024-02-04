import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phone_checker.settings')

app = Celery('phone_checker')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def debug_error_task():
    print('debug')
    raise ValueError('debug error task')
