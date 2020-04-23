import os

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.server')

app = Celery('tasks', broker='pyamqp://guest@localhost/')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

app.conf.accept_content = {'json', 'pickle'}
app.conf.task_serializer = 'pickle'
app.conf.worker_prefetch_multiplier = 1
app.conf.task_ignore_result = True
app.conf.worker_hijack_root_logger = False

app.conf.task_soft_time_limit = 60

app.conf.task_queue_max_priority = 20
app.conf.task_default_priority = 0

app.conf.broker_transport_options = {'confirm_publish': True}

app.conf.timezone = settings.TIME_ZONE

app.conf.task_routes = {
    '*': {'queue': 'celery'},
}
