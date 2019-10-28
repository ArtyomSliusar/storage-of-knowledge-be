from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from main.api.filters import NoteFilter, LinkFilter
from main.api.permissions import IsCreationOrIsAuthenticated
from main.api.serializers import SubjectSerializer, UserSerializer, RefreshTokenSerializer, ContactSerializer, \
    NoteListSerializer, LinkListSerializer, SuggestionsSerializer
from main.documents import NoteDocument, LinkDocument
from main.models import Subject, Note, Link


class ContactView(GenericAPIView):
    serializer_class = ContactSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubjectList(ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


# 1. NOT authenticated:
    # - LIST - only public
    # - RETRIEVE - only public
    # - EDIT - none
    # - DELETE - none
# 2. authenticated:
    # - LIST - all public AND private owned
    # - RETRIEVE - all public AND private owned
    # - EDIT - private owned
    # - DELETE - private owned
class NoteList(ListAPIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]
    serializer_class = NoteListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NoteFilter
    pagination_class = LimitOffsetPagination
    ordering_fields = ['title', 'user', 'likes_count', 'date_modified']

    def get_queryset(self):
        queryset = Note.objects.filter(private=False)

        if self.request.user.is_authenticated:
            private_queryset = Note.objects.filter(private=True, user=self.request.user)
            queryset = queryset | private_queryset  # union

        search_query = self.request.query_params.get('search', None)
        if search_query:
            q = NoteDocument.build_query(search_query)
            search_results = NoteDocument.search().query(q)[:100]  # return top 100
            queryset = queryset & search_results.to_queryset()  # intersection

        qs = queryset.annotate(likes_count=Count('likes'))
        return qs


class NoteSuggestions(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        suggestions = []
        query = request.query_params.get('query', None)

        if query:
            es_suggestions = NoteDocument.search().suggest('suggestions', query, completion={'field': 'title_suggestions'}).execute()

            # can't properly filter suggestions using context suggester, because of the issue:
            # https://github.com/elastic/elasticsearch/issues/30884
            # that is why have to filter suggestions after retrieving them from ES
            if self.request.user.is_authenticated:
                available_notes = {note.str_id for note in self.request.user.available_notes}
            else:
                available_notes = {note.str_id for note in Note.objects.filter(private=False)}

            suggestions = [o for o in es_suggestions.suggest.suggestions[0].options if o._id in available_notes]

        serializer = SuggestionsSerializer(suggestions)
        return Response(serializer.data)


class LinkSuggestions(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        suggestions = []
        query = request.query_params.get('query', None)

        if query:
            es_suggestions = LinkDocument.search().suggest('suggestions', query, completion={'field': 'title_suggestions'}).execute()

            # can't properly filter suggestions using context suggester, because of the issue:
            # https://github.com/elastic/elasticsearch/issues/30884
            # that is why have to filter suggestions after retrieving them from ES
            if self.request.user.is_authenticated:
                available_links = {link.str_id for link in self.request.user.available_links}
            else:
                available_links = {link.str_id for link in Link.objects.filter(private=False)}

            suggestions = [o for o in es_suggestions.suggest.suggestions[0].options if o._id in available_links]

        serializer = SuggestionsSerializer(suggestions)
        return Response(serializer.data)


class LinkList(ListAPIView):
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]
    serializer_class = LinkListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LinkFilter
    pagination_class = LimitOffsetPagination
    ordering_fields = ['title', 'user', 'likes_count', 'date_modified']

    def get_queryset(self):
        queryset = Link.objects.filter(private=False)

        if self.request.user.is_authenticated:
            private_queryset = Link.objects.filter(private=True, user=self.request.user)
            queryset = queryset | private_queryset  # union

        search_query = self.request.query_params.get('search', None)
        if search_query:
            q = LinkDocument.build_query(search_query)
            search_results = LinkDocument.search().query(q)[:100]  # return top 100
            queryset = queryset & search_results.to_queryset()  # intersection

        qs = queryset.annotate(likes_count=Count('likes'))
        return qs


class UserViewSet(ViewSet):
    permission_classes = [IsCreationOrIsAuthenticated]
    renderer_classes = [JSONRenderer]
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = get_user_model().objects.all()
        user = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, user)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
