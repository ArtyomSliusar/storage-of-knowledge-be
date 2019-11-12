from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('notes/<note_id>/comments/<id>', NoteCommentView.as_view(), name='note-comment-instance'),
    path('links/<link_id>/likes/<id>', LinkLikeView.as_view(), name='link-like-instance'),
    path('notes/<note_id>/likes/<id>', NoteLikeView.as_view(), name='note-like-instance'),
    path('notes/<pk>/comments/', NoteCommentCollectionView.as_view(), name='note-instance-comments'),
    path('notes/<pk>/likes/', NoteLikeCollectionView.as_view(), name='note-instance-likes'),
    path('links/<pk>/likes/', LinkLikeCollectionView.as_view(), name='link-instance-likes'),
    path('notes/<pk>', NoteView.as_view(), name='note-instance'),
    path('links/<pk>', LinkView.as_view(), name='link-instance'),
    path('subjects/', SubjectList.as_view(), name='subjects-list'),
    path('notes/', NoteCollectionView.as_view(), name='notes-collection'),
    path('links/', LinkCollectionView.as_view(), name='links-collection'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('suggestions/', Suggestions.as_view(), name='suggestions'),
    path('', include(router.urls)),
]
