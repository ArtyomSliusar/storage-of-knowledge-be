from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('subjects/', SubjectList.as_view(), name='subjects-list'),
    path('notes/', NoteCollectionView.as_view(), name='notes-collection'),
    path('notes/<note_id>/likes/<id>', NoteLikeView.as_view(), name='note-like-instance'),
    path('notes/<pk>/likes/', NoteLikeCollectionView.as_view(), name='note-instance-likes'),
    path('notes/<pk>', NoteView.as_view(), name='note-instance'),
    path('links/', LinkCollectionView.as_view(), name='links-collection'),
    path('links/<link_id>/likes/<id>', LinkLikeView.as_view(), name='link-like-instance'),
    path('links/<pk>/likes/', LinkLikeCollectionView.as_view(), name='link-instance-likes'),
    path('links/<pk>', LinkView.as_view(), name='link-instance'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('suggestions/', Suggestions.as_view(), name='suggestions'),
    path('', include(router.urls)),
]
