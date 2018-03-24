from .base import *


ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='{{ cookiecutter.domain_name }}').split(',')

# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '{{ cookiecutter.project_slug }}' + ' <' + EMAIL_HOST_USER + '>'

# SECURITY
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# STORAGE CONFIGURATION
# pip install boto3 django-storages
# INSTALLED_APPS += ['storages',]
#
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_BUCKET')
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_PRELOAD_METADATA = True
# AWS_S3_FILE_OVERWRITE = False
# AWS_LOCATION = 'media'
# MEDIA_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
#
# # AWS Caching - be careful
# AWS_EXPIRY = 60 * 60 * 24 * 7 # 1 week
# AWS_S3_OBJECT_PARAMETERS = {
#     'Cache-Control': 'max-age={:d}, s-maxage={:d}, must-revalidate'.format(AWS_EXPIRY, AWS_EXPIRY)
# }
# Use this if you have problems with Frankfurt S3 region
# os.environ['S3_USE_SIGV4'] = 'True'
# AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'


# CACHING
CACHES = {
    "default": {
        "BACKEND": 'django_redis.cache.RedisCache',
        "LOCATION": 'redis://127.0.0.1:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
            "IGNORE_EXCEPTIONS": True
        }
    }
}

# SESSIONS
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

#LOGGING
LOG_DIR = PROJECT_ROOT.path('logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
{% if cookiecutter.use_sentry == 'y' %}
    'root': {
        'level': 'ERROR',
        'handlers': ['sentry'],
    },
{% endif %}
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'server': {
            'format': '[%(asctime)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'application': {
            'format': '<%(filename)s> [%(asctime)s] [%(levelname)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        }
    },
    'handlers': {
{% if cookiecutter.use_sentry == 'y' %}
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
        },
{% endif %}
        'errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'server',
            'filename': LOG_DIR('errors.log')
        },
        'access': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'd',
            'interval': 1,
            'backupCount': 2,
            'formatter': 'server',
            'filename': LOG_DIR('access.log')
        },
{% if cookiecutter.use_celery == 'y' %}
        'celery_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'd',
            'interval': 1,
            'backupCount': 2,
            'formatter': 'default',
            'filename': LOG_DIR('celery.log')
        },
{% endif %}
        'app': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'd',
            'interval': 3,
            'backupCount': 2,
            'formatter': 'application',
            'filename': LOG_DIR('app.log')
        },
    },
    'loggers': {
        'app': {
            'handlers': ['app'],
            'level': 'DEBUG',
        },
{% if cookiecutter.use_sentry == 'y' %}
        'celery_tasks': {
            'handlers': ['celery_log'],
            'level': 'DEBUG',
        },
        'celery': {
            'handlers': ['celery_log'],
            'level': 'INFO',
        },
{% endif %}
        'django.request': {
            'handlers': ['errors'],
            'level': 'WARNING',
        },
        'gunicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

{% if cookiecutter.use_sentry == 'y' %}
INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]
RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN'),
    'release': raven.fetch_git_sha(PROJECT_ROOT),
}
{% endif %}
