import sys
from logging.config import dictConfig

import environ
from corsheaders.defaults import default_headers
from django.utils import timezone


DJANGO_ROOT = environ.Path(__file__) - 3
sys.path.insert(0, DJANGO_ROOT('apps'))

env = environ.Env()
environ.Env.read_env(DJANGO_ROOT('.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = ['*']

# APP CONFIGURATION
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_yasg',
    'django_handy',
    'corsheaders',
    'django_filters',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'shared',
    'users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

TEST_RUNNER = 'django_handy.tests.FixedDiscoverRunner'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# GENERAL CONFIGURATION
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SILENCED_SYSTEM_CHECKS = [
    # Security headers set through nginx,
    'security.W002',
    'security.W004',
    'security.W006',
    'security.W007',
    'security.W008',
]

# DATABASES
DATABASE_URL = env('DATABASE_URL')
DATABASES = {
    'default': env.db(),
}
DATABASES['default']['CONN_MAX_AGE'] = 600

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [DJANGO_ROOT('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'string_if_invalid': '[%s]',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    }
]

# FILE CONFIGURATION
STATIC_ROOT = DJANGO_ROOT('staticfiles')
STATICFILES_DIRS = [
    DJANGO_ROOT('static'),
]
STATIC_URL = '/api/static/'

MEDIA_ROOT = DJANGO_ROOT('media')
MEDIA_URL = '/api/media/'

FILE_UPLOAD_PERMISSIONS = 0o644

# URL Configuration
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# AUTH
AUTH_USER_MODEL = 'users.User'

# CORS settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
    'cache-control',
    'pragma',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'django_handy.rest.exceptions.custom_exception_handler',
}
SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': timezone.timedelta(days=30),
}

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] <%(filename)s>:[%(lineno)d] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
    },
}
dictConfig(LOGGING)
