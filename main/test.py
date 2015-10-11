__author__ = 'Artem'
# from models import Publisher
#
# # from wed_project.main.books.views import current_datetime, hours_ahead
# #
# # current_datetime('')
#
#
# publisher_info = {
#     "queryset": Publisher.objects.all(),
# }
#
#
# print publisher_info




#SECRET_KEY = os.environ['HOME']

# for i in os.environ.items():
#     print i

# import os
#
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#
# print  BASE_DIR

a = [[['a']]]

def rec(input):
    if type(input) is list:
        print '1'
        rec(input[0])
    else:
        print input

rec(a)