import os
from configurations import Configuration, values


# TODO: finish 12 factor
class Settings(Configuration):

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = values.ListValue([])

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # Database
    DATABASES = {
        'default': {
            'ENGINE': values.Value(environ_name='DB_ENGINE'),
            'NAME': values.Value(environ_name='DB_NAME'),
            'USER': values.Value(environ_name='DB_USER'),
            'PASSWORD': values.Value(environ_name='DB_PASSWORD'),
            'HOST': values.Value(environ_name='DB_HOST'),
            'PORT': values.Value(environ_name='DB_PORT'),
        }
    }

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_ROOT_DIR = os.path.dirname(BASE_DIR)

    ADMINS = (('artyomsliusar', 'artyomsliusar@gmail.com'),)

    AUTH_USER_MODEL = "main.User"

    LOGIN_REDIRECT_URL = ('/home/')
    LOGIN_URL = '/login/'

    # Application definition
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
        'rest_framework.authtoken',
        # Local apps
        'main.apps.MainConfig'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # custom exception handler
        'main.middleware.timezone_middleware.TimezoneMiddleware',
    ]

    ROOT_URLCONF = 'storageofknowledge.urls'

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
                ],
            },
        },
    ]

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    WSGI_APPLICATION = 'storageofknowledge.wsgi.application'

    # Password validation
    # https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
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

    # Internationalization
    # https://docs.djangoproject.com/en/1.11/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Email
    EMAIL_BACKEND = values.Value()
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_HOST_USER = 'StorageOfKnowledge@gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    DEFAULT_FROM_EMAIL = 'StorageOfKnowledge <noreply@storageofknowledge.com>'
    SERVER_EMAIL = 'StorageOfKnowledge <noreply@storageofknowledge.com>'

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    # --- LOGGING CONFIGURATION --- :
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    }
