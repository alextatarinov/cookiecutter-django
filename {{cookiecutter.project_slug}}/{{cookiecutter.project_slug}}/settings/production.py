from .base import *


ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '{{ cookiecutter.domain_name }}').split(',')

# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', ''),
        'CONN_MAX_AGE': 600
    }
}

# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '{{ cookiecutter.project_slug }}'.capitalize() + ' <' +  EMAIL_HOST_USER + '>'

# SECURITY
{% if cookiecutter.use_ssl == 'y' %}
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_PRELOAD = True
# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
{% else %}
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_HSTS_PRELOAD = True
# # set this to 60 seconds and then to 518400 when you can prove it works
# SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
{% endif %}

{% if cookiecutter.use_s3 == 'y' %}
# STORAGE CONFIGURATION
from storages.backends.s3boto import S3BotoStorage
INSTALLED_APPS += ['storages', 'django_s3_collectstatic']

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
StaticRootS3BotoStorage = lambda: S3BotoStorage(location=STATICFILES_LOCATION)
STATIC_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = '{{ cookiecutter.project_slug }}.settings.production.StaticRootS3BotoStorage'

MEDIAFILES_LOCATION = 'media'
MediaRootS3BotoStorage = lambda: S3BotoStorage(location=MEDIAFILES_LOCATION)
MEDIA_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

DEFAULT_FILE_STORAGE = '{{ cookiecutter.project_slug }}.settings.production.MediaRootS3BotoStorage'
AWS_PRELOAD_METADATA = True

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
control = 'max-age={:d}, s-maxage={:d}, must-revalidate'.format(AWS_EXPIRY, AWS_EXPIRY)
AWS_HEADERS = {
    'Cache-Control': bytes(control, encoding='latin-1')
}

# Use this if you have problems with Frankfurt S3 region
# os.environ['S3_USE_SIGV4'] = 'True'
# AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'
{% endif %}

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
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
{% if cookiecutter.use_sentry_for_error_reporting == 'y' %}
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
{% if cookiecutter.use_sentry_for_error_reporting == 'y' %}
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
            'filename': os.path.join(LOG_DIR, 'errors.log')
        },
        'access': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'd',
            'interval': 1,
            'backupCount': 2,
            'formatter': 'server',
            'filename': os.path.join(LOG_DIR, 'access.log')
        },
{% if cookiecutter.use_celery == 'y' %}
        'celery_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'd',
            'interval': 1,
            'backupCount': 2,
            'formatter': 'default',
            'filename': os.path.join(LOG_DIR, 'celery.log')
        },
{% endif %}
        'app': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'd',
            'interval': 3,
            'backupCount': 2,
            'formatter': 'application',
            'filename': os.path.join(LOG_DIR, 'app.log')
        },
    },
    'loggers': {
        'app': {
            'handlers': ['app'],
            'level': 'DEBUG',
        },
{% if cookiecutter.use_sentry_for_error_reporting == 'y' %}
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

{% if cookiecutter.use_sentry_for_error_reporting == 'y' %}
INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]
RAVEN_CONFIG = {
    'dsn': os.environ.get('DJANGO_SENTRY_DSN'),
    'release': raven.fetch_git_sha(PROJECT_ROOT),
}
{% endif %}
