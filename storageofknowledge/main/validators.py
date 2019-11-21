import pytz
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
