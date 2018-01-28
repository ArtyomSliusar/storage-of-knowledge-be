import os
from configurations import Configuration


class CommonSettings(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    PROJECT_ROOT_DIR = os.path.dirname(BASE_DIR)

    ADMINS = (('artyomsliusar', 'artyomsliusar@gmail.com'),)

    LOGIN_REDIRECT_URL = ('/home/')
    LOGIN_URL = '/login/'

    # Application definition
    INSTALLED_APPS = [
        # Django apps
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Third party
        'ckeditor',
        'django_wysiwyg',
        'django_requestlogging',
        # Local apps
        'main.apps.MainConfig'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # third party
        'request_logging.middleware.LoggingMiddleware',
        # custom exception handler
        'main.middleware.timezone_middleware.TimezoneMiddleware',
    ]

    ROOT_URLCONF = 'storageofknowledge.urls'
    AUTH_PROFILE_MODULE = "storageofknowledge.UserProfile"

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
    DJANGO_WYSIWYG_FLAVOR = 'ckeditor'  # Requires you to also place the ckeditor files here:
    DJANGO_WYSIWYG_MEDIA_URL = STATIC_URL + "ckeditor/"
    CKEDITOR_UPLOAD_PATH = "uploads/"

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