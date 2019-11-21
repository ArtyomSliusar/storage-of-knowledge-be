import pytz
from django.contrib.auth import get_user_model
from pytz import UnknownTimeZoneError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_time_zone(value):
    try:
        pytz.timezone(value)
    except UnknownTimeZoneError:
        raise ValidationError(
            _('%(value)s is not a valid time zone'),
            params={'value': value},
        )


def validate_email(email, exclude_username=None):
    email_queryset = get_user_model().objects.filter(email=email)
    if exclude_username:
        email_queryset = email_queryset.exclude(username=exclude_username)

    if email_queryset.exists():
        raise ValidationError(
            _('User with this email already exists')
        )
