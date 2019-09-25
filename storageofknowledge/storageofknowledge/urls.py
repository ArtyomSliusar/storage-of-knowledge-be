from django.conf.urls import url, include
from django.contrib import admin


admin.site.site_header = 'Storage Of Knowledge Admin'
admin.site.site_title = 'Storage Of Knowledge'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include("main.api.urls")),
    url(r'^', include('main.urls')),
]
