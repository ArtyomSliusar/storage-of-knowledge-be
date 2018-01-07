__author__ = 'Artem Sliusar'


import pytz
from django.utils import timezone


class TimezoneMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        tzname = None
        if request.user.is_authenticated():
            user_profile = request.user.profile
            tzname = user_profile.time_zone
        if tzname:
            timezone.activate(pytz.timezone(tzname))

