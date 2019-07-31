"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import dotenv

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
settings_to_use = os.getenv('DJANGO_SETTINGS')

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "storageofknowledge.settings.{settings}".format(
        settings=settings_to_use
    )
)

os.environ.setdefault(
        'DJANGO_CONFIGURATION',
        '{settings}Settings'.format(
            settings=settings_to_use.capitalize()
        )
    )

from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()
