#!/usr/bin/env python
import os
import sys
import dotenv


dotenv.read_dotenv()


if __name__ == "__main__":
    settings_to_use = os.getenv('SETTINGS')

    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'storageofknowledge.settings.{settings}'.format(
            settings=settings_to_use
        )
    )
    os.environ.setdefault(
        'DJANGO_CONFIGURATION',
        '{settings}Settings'.format(
            settings=settings_to_use.capitalize()
        )
    )

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
