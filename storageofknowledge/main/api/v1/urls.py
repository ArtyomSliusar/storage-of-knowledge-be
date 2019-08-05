from django.urls import path
from .views import *

urlpatterns = [
    path('subjects/', SubjectList.as_view(), name='subject-list'),
]
