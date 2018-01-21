import os
from configurations import values
from .common import CommonSettings


class ProductionSettings(CommonSettings):

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['.storageofknowledge.com']

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(CommonSettings.BASE_DIR, 'production.sqlite3'),
        }
    }

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    # TODO: secret password
    EMAIL_HOST_PASSWORD = ''
    EMAIL_HOST_USER = 'StorageOfKnowledge@gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'StorageOfKnowledge <noreply@storageofknowledge@gmail.com>'
    SERVER_EMAIL = 'StorageOfKnowledge <noreply@storageofknowledge@gmail.com>'

    STATIC_ROOT = os.path.join(CommonSettings.BASE_DIR, 'staticfiles')

    # --- LOGGING CONFIGURATION --- :
    # TODO: configure logging
    LOGGING_CONFIG = None
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
        },
        'formatters': {
            'default': {
                'format': '[%(asctime)s] | %(levelname)s | %(message)s | '
                          '%(remote_addr)s | %(username)s | %(request_method)s | '
                          '%(path_info)s | %(server_protocol)s | %(http_user_agent)s'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': False,
            },
            # 'request_handler': {
            #     'level': 'WARNING',
            #     'class': 'logging.handlers.RotatingFileHandler',
            #     'filename': PROJECT_ROOT_DIR + '/log/django_request.log',
            #     'maxBytes': 1024 * 1024 * 5,  # 5 MB
            #     'backupCount': 5,
            #     'filters': ['request'],
            #     'formatter': 'default',
            # },
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                # 'filters': ['request'],
                'propagate': False,
            },
        }
    }
    import logging.config
    logging.config.dictConfig(LOGGING)
