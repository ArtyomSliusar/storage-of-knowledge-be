from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('subjects/', SubjectList.as_view(), name='subjects-list'),
    path('notes/suggestions/', NoteSuggestions.as_view(), name='notes-suggestions'),
    path('links/suggestions/', LinkSuggestions.as_view(), name='links-suggestions'),
    path('notes/', NoteCollectionView.as_view(), name='notes-collection'),
    path('notes/<pk>', NoteView.as_view(), name='note-instance'),
    path('links/', LinkCollectionView.as_view(), name='links-collection'),
    path('links/<pk>', LinkView.as_view(), name='link-instance'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('', include(router.urls)),
]
