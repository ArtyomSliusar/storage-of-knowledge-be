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
