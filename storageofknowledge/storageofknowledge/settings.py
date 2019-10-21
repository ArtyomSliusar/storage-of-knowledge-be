import json
import os
from datetime import timedelta
from configurations import Configuration, values


ENVIRONMENT = values.Value(environ_name='ENVIRONMENT')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT_DIR = os.path.dirname(BASE_DIR)


def logging_config():
    """If DJANGO_LOGGING_CONFIG_FILE is not set, default django logging config is used"""
    var_name = 'LOGGING_CONFIG_FILE'

    if os.environ.get('DJANGO_' + var_name):
        with open(values.PathValue(environ_name=var_name)) as f:
            content = f.read()
            content = content.replace('{project_root}', PROJECT_ROOT_DIR)
            return json.loads(content)


class Settings(Configuration):
    ADMIN_HEADER_COLOR = values.Value()
    ADMIN_HEADER_TITLE = "{environment}{title}".format(
        environment=ENVIRONMENT or '{DJANGO_ENVIRONMENT}',
        title=values.Value('{DJANGO_ADMIN_HEADER_TITLE}', environ_name='ADMIN_HEADER_TITLE'),
    )
    ADMINS = values.SingleNestedListValue([])
    ALLOWED_HOSTS = values.ListValue([])
    ANYMAIL = values.DictValue()
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
    AUTH_USER_MODEL = "main.User"
    CORS_ORIGIN_WHITELIST = values.ListValue([])
    DATABASES = values.DatabaseURLValue(environ_prefix='DJANGO')
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)
    DEFAULT_FROM_EMAIL = 'StorageOfKnowledge <noreply@storageofknowledge.com>'
    EMAIL_BACKEND = values.Value()
    EMAIL_HOST = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_HOST_USER = values.Value()
    EMAIL_PORT = values.Value()
    EMAIL_USE_TLS = values.BooleanValue(False)
    INSTALLED_APPS = [
        # Django apps
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Third party
        'django_extensions',
        'rest_framework',
        'rest_framework_simplejwt.token_blacklist',
        'corsheaders',
        'django_filters',
        # Local apps
        'main.apps.MainConfig'
    ]
    LANGUAGE_CODE = values.Value('en-us')
    LOGGING = logging_config()
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # custom exception handler
        'main.middleware.timezone_middleware.TimezoneMiddleware',
    ]
    REST_FRAMEWORK = {
        'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'PAGE_SIZE': 50,
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    }
    ROOT_URLCONF = 'storageofknowledge.urls'
    SECRET_KEY = values.SecretValue()
    SERVER_EMAIL = 'StorageOfKnowledge <noreply@storageofknowledge.com>'
    SESSION_COOKIE_AGE = values.IntegerValue(5 * 60)  # 5 minutes
    SESSION_SAVE_EVERY_REQUEST = values.BooleanValue(True)
    SIMPLE_JWT = {
        'ROTATE_REFRESH_TOKENS': True,
    }
    STATIC_ROOT = values.Value(None)
    STATIC_URL = '/static/'
    STATICFILES_DIRS = values.SingleNestedListValue([])
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                (os.path.join(BASE_DIR, "templates"))
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.media',
                    'main.context_processors.from_settings',
                ],
            },
        },
    ]
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    WSGI_APPLICATION = 'storageofknowledge.wsgi.application'
