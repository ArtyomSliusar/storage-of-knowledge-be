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

# a = [[['a']]]
#
# def rec(input):
#     if type(input) is list:
#         print '1'
#         rec(input[0])
#     else:
#         print input
#
# rec(a)
#
query = 'dg'

text = 'fdsfs fsdgdf query gfd jhgfjg'


st = fn = False

beg = text.find(query)

n = 0
while st is False:
    n += 1
    ind = beg-n
    if ind <= 0:
        start = 0
        break
    start = text[ind]
    if not start.isalpha():
        start = ind
        st = True
n = 0
while fn is False:
    n += 1
    ind = beg+len(query)+n
    if ind >= len(text):
        finish = len(text)
        break
    finish = text[ind]
    if not finish.isalpha():
        finish = ind
        fn = True

subs = text[start:finish]
print subs
