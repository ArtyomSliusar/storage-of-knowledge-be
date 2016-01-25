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
    url('^login/', auth_views.login, {'template_name': 'login/login.html'}, name='login'),
    url('^logout/', 'user_logout', name='logout'),
    url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'reset_password_confirm', name='reset_password_confirm'),
    url(r'^reset_password_done/$', 'reset_password_done', name='reset_password_done'),
    url(r'^reset_password/$', 'reset_password', name='reset_password'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^learn_options/$', 'learn_options', name='learn_options'),
    url(r'^check_options/$', 'check_options', name='check_options'),
    url(r'^note_options/$', 'note_options', name='note_options'),
    url(r'^home/$', 'get_home', name='home'),
    url(r'^api/get_topics/', 'get_topics', name='get_topics'),
    url(r'^search_posts/$', 'search_posts', name='search_posts'),
    url(r'^show_post/$', 'show_post', name='show_post'),
    url(r'^$', 'get_home'),
)
