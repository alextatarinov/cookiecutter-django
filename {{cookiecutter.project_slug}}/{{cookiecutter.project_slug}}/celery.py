import os

from celery import Celery
from django.conf import settings


app = Celery('{{ cookiecutter.project_slug }}', broker='redis://localhost:6379/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ cookiecutter.project_slug }}.settings.local')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Uncomment this if you have long-running tasks
# app.conf.worker_prefetch_multiplier = 1
app.conf.task_ignore_result = True
app.conf.worker_hijack_root_logger = False
app.conf.task_soft_time_limit = 60
app.conf.broker_transport_options = {
    'fanout_prefix': True,
    'fanout_patterns': True,
    'visibility_timeout': 3600  # must exceed maximum task eta/countdown
}

app.conf.task_routes = {
    '*': {'queue': 'celery'}
}