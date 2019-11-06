from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView, get_object_or_404, DestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from main.api.filters import NoteFilter, LinkFilter, NoteLikeFilter, LinkLikeFilter
from main.api.permissions import IsCreationOrIsAuthenticated, IsOwnerOrPublicReadOnly, \
    IsAuthenticatedAndIsOwner
from main.api.serializers import SubjectSerializer, UserSerializer, RefreshTokenSerializer, ContactSerializer, \
    NoteListSerializer, LinkListSerializer, SuggestionsSerializer, NoteSerializer, LinkSerializer, \
    NoteLikeSerializer, LinkLikeSerializer
from main.documents import NoteDocument, LinkDocument, INDEX_DOCUMENT_MAP
from main.models import Subject, Note, Link, NoteLike, LinkLike


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


class Suggestions(GenericAPIView):
    serializer_class = SuggestionsSerializer
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        suggestions = []
        query = request.query_params.get('query', None)
        index = request.query_params.get('index', None)

        document_model = INDEX_DOCUMENT_MAP.get(index)

        if query and document_model:
            suggestions = document_model.get_suggestions(query)

        serializer = self.get_serializer(suggestions)
        return Response(serializer.data)


class NoteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrPublicReadOnly]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()


class NoteLikeView(DestroyAPIView):
    """
    DELETE /notes/{note_id}/likes/{id} - delete note's like (USER AUTHENTICATED AND OWNER OF LIKE)
    """
    permission_classes = [IsAuthenticatedAndIsOwner]
    serializer_class = NoteLikeSerializer
    lookup_fields = ['note_id', 'id']
    queryset = NoteLike.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class NoteLikeCollectionView(ListCreateAPIView):
    """
    GET /notes/{id}/likes - return list of note's likes (USER AUTHENTICATED)
    GET /notes/{id}/likes?user={id} - return list of note's likes done by specified user (USER AUTHENTICATED)
    POST /notes/{id}/likes - create like for note and user (USER AUTHENTICATED)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteLikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NoteLikeFilter

    def get_queryset(self):
        note = get_object_or_404(Note, **self.kwargs)
        return NoteLike.objects.filter(note=note)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                "note": kwargs['pk'],
                "user": request.user.id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


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


class LinkLikeView(DestroyAPIView):
    """
    DELETE /links/{link_id}/likes/{id} - delete link's like (USER AUTHENTICATED AND OWNER OF LIKE)
    """
    permission_classes = [IsAuthenticatedAndIsOwner]
    serializer_class = LinkLikeSerializer
    lookup_fields = ['link_id', 'id']
    queryset = LinkLike.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class LinkLikeCollectionView(ListCreateAPIView):
    """
    GET /links/{id}/likes - return list of link's likes (USER AUTHENTICATED)
    GET /links/{id}/likes?user={id} - return list of link's likes done by specified user (USER AUTHENTICATED)
    POST /links/{id}/likes - create like for link and user (USER AUTHENTICATED)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LinkLikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LinkLikeFilter

    def get_queryset(self):
        link = get_object_or_404(Link, **self.kwargs)
        return LinkLike.objects.filter(link=link)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                "link": kwargs['pk'],
                "user": request.user.id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


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
