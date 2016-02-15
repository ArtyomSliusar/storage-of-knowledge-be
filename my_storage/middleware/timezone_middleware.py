__author__ = 'Artem Sliusar'


import pytz
from django.utils import timezone


class TimezoneMiddleware(object):

    def process_request(self, request):
        tzname = None
        if request.user.is_authenticated():
            user_profile = request.user.profile
            tzname = user_profile.time_zone
        if tzname:
            timezone.activate(pytz.timezone(tzname))

