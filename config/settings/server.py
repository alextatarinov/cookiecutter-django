# noinspection PyUnresolvedReferences
import sys
# noinspection PyUnresolvedReferences
from logging.config import dictConfig

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from config.settings.base import *  # noqa: F401, F403, WPS347
from config.settings.base import DJANGO_ROOT, LOGGING, env


# Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = False

# LOGGING
LOG_DIR = DJANGO_ROOT.path('logs')
SENTRY_DNS = env('SENTRY_DNS')

# Don't enable sentry for shell
if 'shell' not in sys.argv:
    sentry_sdk.init(
        dsn=SENTRY_DNS,
        integrations=[DjangoIntegration(), RedisIntegration(), CeleryIntegration()],
        send_default_pii=True,
    )

file_handler = {
    'level': 'INFO',
    'formatter': 'standard',
    'class': 'mrfh.MultiprocessRotatingFileHandler',
    'maxBytes': 10 * 1024 * 1024,  # 10 MB
    'backupCount': 1,
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['app'],
    },
    'handlers': {
        'app': {
            **file_handler,
            'filename': LOG_DIR('app.log'),
        },
        'access': {
            **file_handler,
            'filename': LOG_DIR('access.log'),
        },
        'celery': {
            **file_handler,
            'filename': LOG_DIR('celery.log'),
        },
    },
    'loggers': {
        'gunicorn': {
            'level': 'INFO',
            'handlers': ['access'],
            'propagate': False,
        },
        'celery': {
            'level': 'DEBUG',
            'handlers': ['celery'],
            'propagate': False,
        },
    },
    'formatters': LOGGING['formatters'],
}
dictConfig(LOGGING)

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = f'4Challenge <{EMAIL_HOST_USER}>'

# SECURITY
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CACHE
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        },
    },
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
