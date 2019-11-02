from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from main.api.filters import NoteFilter, LinkFilter
from main.api.permissions import IsCreationOrIsAuthenticated, IsOwnerOrPublicReadOnly
from main.api.serializers import SubjectSerializer, UserSerializer, RefreshTokenSerializer, ContactSerializer, \
    NoteListSerializer, LinkListSerializer, SuggestionsSerializer, NoteSerializer, LinkSerializer
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
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class NoteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrPublicReadOnly]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class NoteCollectionView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NoteFilter
    pagination_class = LimitOffsetPagination
    ordering_fields = ['title', 'user', 'likes_count', 'date_modified']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            available_notes = self.request.user.available_notes
        else:
            available_notes = Note.objects.filter(private=False)

        search_query = self.request.query_params.get('search', None)
        if search_query:
            q = NoteDocument.build_query(search_query)
            search_results = NoteDocument.search().query(q)[:100]  # return top 100
            available_notes = available_notes & search_results.to_queryset()  # intersection

        return available_notes.annotate(likes_count=Count('likes'))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NoteSerializer
        else:
            return NoteListSerializer


class NoteSuggestions(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        suggestions = []
        query = request.query_params.get('query', None)

        if query:
            es_suggestions = NoteDocument.search().suggest('suggestions', query, completion={'field': 'title_suggestions'}).execute()

            # can't properly filter suggestions using context suggester, because of the issue:
            # https://github.com/elastic/elasticsearch/issues/30884
            # that is why have to filter suggestions after retrieving them from ES
            suggestions = [o for o in es_suggestions.suggest.suggestions[0].options if o['_source'].private is False]

        serializer = SuggestionsSerializer(suggestions)
        return Response(serializer.data)


class LinkView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrPublicReadOnly]
    serializer_class = LinkSerializer
    queryset = Link.objects.all()


class LinkCollectionView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LinkFilter
    pagination_class = LimitOffsetPagination
    ordering_fields = ['title', 'user', 'likes_count', 'date_modified']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            available_links = self.request.user.available_links
        else:
            available_links = Link.objects.filter(private=False)

        search_query = self.request.query_params.get('search', None)
        if search_query:
            q = LinkDocument.build_query(search_query)
            search_results = LinkDocument.search().query(q)[:100]  # return top 100
            available_links = available_links & search_results.to_queryset()  # intersection

        return available_links.annotate(likes_count=Count('likes'))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LinkSerializer
        else:
            return LinkListSerializer


class LinkSuggestions(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        suggestions = []
        query = request.query_params.get('query', None)

        if query:
            es_suggestions = LinkDocument.search().suggest('suggestions', query, completion={'field': 'title_suggestions'}).execute()

            # can't properly filter suggestions using context suggester, because of the issue:
            # https://github.com/elastic/elasticsearch/issues/30884
            # that is why have to filter suggestions after retrieving them from ES
            suggestions = [o for o in es_suggestions.suggest.suggestions[0].options if o['_source'].private is False]

        serializer = SuggestionsSerializer(suggestions)
        return Response(serializer.data)


class UserViewSet(ViewSet):
    permission_classes = [IsCreationOrIsAuthenticated]
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
