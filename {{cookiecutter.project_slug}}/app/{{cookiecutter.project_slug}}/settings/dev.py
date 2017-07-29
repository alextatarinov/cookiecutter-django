from .base import *


# DEBUG
DEBUG = True

# Mail settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-debug-toolbar
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ cookiecutter.project_slug }}',
        'USER': '{{ cookiecutter.project_slug }}',
        'PASSWORD': '{{ cookiecutter.project_slug }}',
        'HOST': '127.0.0.1',
        'PORT': '',
        'CONN_MAX_AGE': 600
    }
}

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
