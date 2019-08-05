from rest_framework import authentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from main.api.serializers import SubjectSerializer
from main.models import Subject


class SubjectList(ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
