__author__ = 'Artem Sliusar'


import pytz
from django.utils import timezone


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
        tzname = None
        if request.user.is_authenticated:
            tzname = request.user.time_zone
        if tzname:
            timezone.activate(pytz.timezone(tzname))
