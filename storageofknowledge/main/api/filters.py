import django_filters
from main.models import Note, Link, Subject


def filter_subjects(queryset, name, value):
    if value.startswith('in:'):
        qs = queryset.filter(subjects__name__in=value.lstrip('in:').split(','))
    else:
        qs = queryset.filter(subjects__name=value)
    return qs


class NoteFilter(django_filters.FilterSet):
    subjects = django_filters.CharFilter(method=filter_subjects)

    class Meta:
        model = Note
        fields = ['subjects']


class LinkFilter(django_filters.FilterSet):
    subjects = django_filters.CharFilter(method=filter_subjects)

    class Meta:
        model = Link
        fields = ['subjects']
