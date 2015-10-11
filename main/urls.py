from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import ListView
from books.models import Publisher
from django.contrib.auth import views as auth_views


urlpatterns = patterns('main.views',
    #(r'^time/$', 'current_datetime'),
    #(r'^time/plus/(\d{1,2})/$', 'hours_ahead'),
    (r'^search/$', 'search'),
    (r'^contact/$', 'contact'),
    (r'thanks$', 'thanks'),
    (r'^add_publisher/$', 'add_publisher'),
    (r'^publishers/$', ListView.as_view(model=Publisher, context_object_name="publisher_list",)),
    url('^register/', 'register', name='register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^learn_options/$', 'show_options', name='learn-options'),
    url(r'^home/$', 'get_home', name='home'),
    url(r'^$', 'get_home'),
)
