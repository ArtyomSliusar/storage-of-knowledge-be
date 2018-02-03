import os
from configurations import values
from .common import CommonSettings


class ProductionSettings(CommonSettings):

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['.storageofknowledge.com']

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue(environ_name="SECRET_KEY")
    DB_USER = values.SecretValue(environ_name="DB_USER")
    DB_PASSWORD = values.SecretValue(environ_name="DB_PASSWORD")

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'storageofknowledge',
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_PASSWORD = values.SecretValue(environ_name="EMAIL_HOST_PASSWORD")
    EMAIL_HOST_USER = 'StorageOfKnowledge@gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'StorageOfKnowledge <noreply@storageofknowledge.com>'
    SERVER_EMAIL = 'StorageOfKnowledge <noreply@storageofknowledge.com>'

    STATIC_ROOT = os.path.join(CommonSettings.BASE_DIR, 'staticfiles')

    # --- LOGGING CONFIGURATION --- :
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'logfile': {
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': '{}/log/app.log'.format(CommonSettings.PROJECT_ROOT_DIR)
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['require_debug_false'],
                'include_html': True,
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django': {
                'handlers': ['logfile', 'console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
    import logging.config
    logging.config.dictConfig(LOGGING)
