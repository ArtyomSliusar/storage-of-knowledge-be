"""
Django settings for project.
For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates').replace('\\', '/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': ["django.template.context_processors.debug",
                                   "django.template.context_processors.request",
                                   "django.contrib.auth.context_processors.auth",
                                   "django.contrib.messages.context_processors.messages",
                                    ]
        },
    },
]

LOGIN_REDIRECT_URL = ('/home/')
LOGIN_URL = '/login/'

# SECURITY WARNING: keep the secret key used in production secret!
with open('secret_keys.txt') as f:
    secret_info = f.read().split()
    SECRET_KEY = secret_info[0]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# TEMPLATE_DEBUG = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_storage',
    'ckeditor',
    'django_wysiwyg',
    'django_requestlogging',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'my_storage.middleware.timezone_middleware.TimezoneMiddleware',
    'django_requestlogging.middleware.LogSetupMiddleware',
)

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'NAME': 'storageo_knowledge',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': secret_info[1],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Email settings:
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'StorageOfKnowledge@gmail.com'

EMAIL_HOST_PASSWORD = secret_info[2]

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SERVER_EMAIL = EMAIL_HOST_USER


ADMINS = (('artyomsliusar', 'artyomsliusar@gmail.com'),)


# Static files settings:
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
)

STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
)


AUTH_PROFILE_MODULE = "my_storage.UserProfile"


# WYSIWYG settings:
DJANGO_WYSIWYG_FLAVOR = 'ckeditor'  # Requires you to also place the ckeditor files here:
# DJANGO_WYSIWYG_MEDIA_URL = STATIC_URL + "ckeditor/"

CKEDITOR_UPLOAD_PATH = "uploads/"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Logging configuration:
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'filters': {
        # Add an unbound RequestFilter.
        'request': {
            '()': 'django_requestlogging.logging_filters.RequestFilter',
        },
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s] | %(levelname)s | %(message)s | %(remote_addr)s | %(username)s | %(request_method)s | '
                      '%(path_info)s | %(server_protocol)s | %(http_user_agent)s'
        },
    },
    'handlers': {
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'include_html': False,
        # },
        'request_handler': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/django_request.log',
                'maxBytes': 1024*1024*5,  # 5 MB
                'backupCount': 5,
                'filters': ['request'],
                'formatter': 'default',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'WARNING',
            'filters': ['request'],
            'propagate': False,
        },
    }
}

import logging.config
logging.config.dictConfig(LOGGING)
