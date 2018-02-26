from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ALLOWED_HOSTS = ['*']
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'naming': {
            'format': '%(name)s: [%(asctime)s] [%(levelname)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'naming'
        }
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
{% if cookiecutter.use_celery == 'y' %}
        'celery_tasks': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
{% endif %}
    }
}
