from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views


urlpatterns = patterns('main.views',
    url('^register/', 'register', name='register'),
    url('^edit_profile/', 'edit_profile', name='edit_profile'),
    url('^login/', auth_views.login, {'template_name': 'login/login.html'}, name='login'),
    url('^logout/', 'user_logout', name='logout'),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'reset_password_confirm', name='reset_password_confirm'),
    url(r'^reset_password_done/$', 'reset_password_done', name='reset_password_done'),
    url(r'^reset_password/$', 'reset_password', name='reset_password'),
    url(r'^learn_options/$', 'learn_options', name='learn_options'),
    url(r'^check_options/$', 'check_options', name='check_options'),
    url(r'^note_options/$', 'note_options', name='note_options'),
    url(r'^home/$', 'get_home', name='home'),
    url(r'^api/get_topics/', 'get_topics', name='get_topics'),
    url(r'^search_notes/$', 'search_notes', name='search_notes'),
    url(r'^add_note/$', 'add_note', name='add_note'),
    url(r'^edit_note/$', 'edit_note', name='edit_note'),
    url(r'^delete_note/$', 'delete_note', name='delete_note'),
    url(r'^show_note/$', 'show_note', name='show_note'),
    url(r'^set_user_timezone/$', 'set_user_timezone', name='set_user_timezone'),
    url(r'^api/add_comment/$', 'add_comment', name='add_comment'),
    url(r'^$', 'get_home'),
)
