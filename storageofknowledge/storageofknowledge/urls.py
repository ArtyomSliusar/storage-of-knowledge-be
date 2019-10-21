from django.conf.urls import include
from django.contrib import admin
from django.urls import path

admin.site.site_header = 'Storage Of Knowledge Admin'
admin.site.site_title = 'Storage Of Knowledge'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("main.api.urls")),
    path('', include('main.urls')),
]
