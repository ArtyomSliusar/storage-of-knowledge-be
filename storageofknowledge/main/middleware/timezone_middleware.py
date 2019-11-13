import pytz
from django.utils import timezone
from pytz import UnknownTimeZoneError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken


class TimezoneMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self._process_timezone(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def _process_timezone(self, request):
        try:
            auth_header = request.META['HTTP_AUTHORIZATION']
            if auth_header.startswith("Bearer"):
                token = AccessToken(auth_header.split()[1])
                timezone.activate(pytz.timezone(token.payload["time_zone"]))
                return
        except (IndexError, KeyError, UnknownTimeZoneError, TokenError):
            pass

        timezone.deactivate()
