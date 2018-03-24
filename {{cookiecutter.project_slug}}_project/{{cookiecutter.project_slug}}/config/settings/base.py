import environ

DJANGO_ROOT = environ.Path(__file__) - 3
PROJECT_ROOT = DJANGO_ROOT - 1

env = environ.Env()
environ.Env.read_env(DJANGO_ROOT('.env'))


SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)

# APP CONFIGURATION
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]

THIRD_PARTY_APPS = [
    {% if cookiecutter.use_drf == 'y' %}'rest_framework',
    'rest_framework_swagger',{% endif %}
    'django_extensions',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'apps.users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# GENERAL CONFIGURATION
TIME_ZONE = '{{ cookiecutter.timezone }}'
LANGUAGE_CODE = '{{ cookiecutter.language_code }}'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DATABASES
DATABASES = {
    'default': env.db()
}
DATABASES['default']['CONN_MAX_AGE'] = 600

# DJANGO DEBUG TOOLBAR
if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    INSTALLED_APPS += ['debug_toolbar',]
    INTERNAL_IPS = ['127.0.0.1']
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }

# TEMPLATE CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [DJANGO_ROOT('templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
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

# STATIC FILE CONFIGURATION
STATIC_ROOT = PROJECT_ROOT('staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    DJANGO_ROOT('static')
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# MEDIA CONFIGURATION
MEDIA_ROOT = PROJECT_ROOT('media')
MEDIA_URL = '/media/'
FILE_UPLOAD_PERMISSIONS = 0o644

# URL Configuration
ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# PASSWORD STORAGE SETTINGS
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
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

# AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Custom user app defaults
AUTH_USER_MODEL = 'users.User'

# Location of root django.contrib.admin URL
ADMIN_URL = 'admin'

# SECURITY
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
