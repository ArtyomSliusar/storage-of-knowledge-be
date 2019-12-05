from django.conf import settings


def from_settings(request):
    """
    Makes application settings available in templates.
    """
    return {
        'ADMIN_HEADER_TITLE': settings.ADMIN_HEADER_TITLE,
        'ADMIN_HEADER_COLOR': settings.ADMIN_HEADER_COLOR,
    }
