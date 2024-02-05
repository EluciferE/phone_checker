import os
from datetime import timedelta

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_IMPORTS = ('checker_base.tasks.sync_phones',)

CELERY_BEAT_SCHEDULE = {
    'sync_phone_numbers': {'task': 'checker_base.tasks.sync_phone_numbers', 'schedule': timedelta(minutes=10)},
}
