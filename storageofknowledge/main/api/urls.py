from django.conf.urls import url, include
from rest_framework.authtoken import views


urlpatterns = [
    url(r'token-auth/', views.obtain_auth_token),
    url(r'v1/', include(('main.api.v1.urls', 'v1'), namespace='v1')),
]
