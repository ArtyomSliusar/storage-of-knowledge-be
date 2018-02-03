import os
from configurations import values
from .common import CommonSettings


class DevelopmentSettings(CommonSettings):

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['*']

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(CommonSettings.BASE_DIR, 'development.sqlite3'),
        }
    }

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue(environ_name="SECRET_KEY")

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # --- LOGGING CONFIGURATION --- :
    # TODO: configure logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'formatters': {
            'verbose': {
                'format': '[%(asctime)s] | %(levelname)s | %(message)s | '
                          '%(remote_addr)s | %(username)s | %(request_method)s | '
                          '%(path_info)s | %(server_protocol)s | %(http_user_agent)s'
            },
            'simple': {
                'format': '%(levelname)s {%(name)s} %(message)s'
            },
            'timestamped': {
                'format': '%(levelname)s %(asctime)s {%(name)s} %(message)s'
            },
        },
        'handlers': {
            'req_res_dump_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': CommonSettings.PROJECT_ROOT_DIR + '/log/django_request.log',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'formatter': 'timestamped',
            },
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'timestamped'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['req_res_dump_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'INFO'
            },
            'django.server': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'INFO'
            },
        }
    }
    import logging.config
    logging.config.dictConfig(LOGGING)
