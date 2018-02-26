import os

from celery import Celery
from django.conf import settings


app = Celery('{{ cookiecutter.project_slug }}', broker='amqp://guest@localhost//')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Uncomment this if you have long-running tasks
# app.conf.worker_prefetch_multiplier = 1
app.conf.task_ignore_result = True
app.conf.worker_hijack_root_logger = False
app.conf.task_soft_time_limit = 60

app.conf.task_routes = {
    '*': {'queue': 'celery'}
}
