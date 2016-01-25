from django.db.models import Q
from django.shortcuts import render_to_response
from books.models import Book, Post
from books.forms import ContactForm, PublisherForm, UserForm, PostForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from main import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
import json


def search(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
        Q(title__icontains=query) |
        Q(authors__first_name__icontains=query) |
        Q(authors__last_name__icontains=query)
        )
        results = Book.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("books/search.html", {"results": results, "query": query})


def search_posts(request):

    form = PostForm(request.GET, empty_permitted=True)
    topic_results = []
    body_results = []
    if form.is_valid():
        subject = request.GET.get('subject', '')
        topic = request.GET.get('topic', '')
        topic_qset = (Q(private=0))
        body_qset = (Q(private=0))

        if request.user.is_authenticated():
            username = request.user.username
            user_id = User.objects.get(username=username)
            topic_qset.add(Q(user_id=user_id), Q.OR)
            body_qset.add(Q(user_id=user_id), Q.OR)

        if subject:
            topic_qset.add(Q(subject=subject), Q.AND)
            body_qset.add(Q(subject=subject), Q.AND)
        if topic:
            topic_qset.add(Q(topic__icontains=topic), Q.AND)
            body_qset.add(Q(body__icontains=topic), Q.AND)
        else:
            body_qset = []

        topic_results = Post.objects.filter(topic_qset).distinct()

        if body_qset:
            body_results = Post.objects.filter(body_qset).distinct()
            body_results = set(body_results) - set(topic_results)

    return render_to_response("note_options/note_options.html", {'form': form, "topic_results": topic_results,
                                                                 "body_results": body_results, "query": True}, RequestContext(request))


def show_post(request):
    post_id = int(request.GET.get('id', ''))
    post = Post.objects.get(id=post_id)
    error = ''
    if post.private == 1:
        if request.user.is_authenticated():
            username = request.user.username
            user_id = User.objects.get(username=username).id
            if post.user_id != user_id:
                error = 'This post is private, only author can view this post.'
                post = []
        else:
            error = 'This post is private, please login.'
            post = []
    return render_to_response('posts/show_post.html', {'post': post, 'error': error}, RequestContext(request))


def get_home(request):
    return render_to_response("home/index.html", RequestContext(request))


def learn_options(request):
    return render_to_response("learn_options/learn_options.html", RequestContext(request))


def check_options(request):
    return render_to_response("check_options/check_options.html", RequestContext(request))


def note_options(request):
    form = PostForm()
    return render_to_response("note_options/note_options.html", {'form': form}, RequestContext(request))


def get_topics(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        qset = (Q(topic__icontains=query))
        if request.user.is_authenticated():
            username = request.user.username
            user_id = User.objects.get(username=username)
        else:
            user_id = None
        extra_param = request.GET.get('subject', '')
        if extra_param:
            qset.add(Q(subject=extra_param), Q.AND)
        posts = Post.objects.filter(qset, Q(private=0) | Q(user_id=user_id))[:20]
        results = []
        for post in posts:
            results.append(post.topic)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)




# def current_datetime(request):
#     now = datetime.datetime.now()
#     return render_to_response("datetime/current_datetime.html", {'current_date': now})


# def user_login(request):
#     redirect_to = request.REQUEST.get('next', '/home/')
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(redirect_to, RequestContext(request))
#             else:
#                 HttpResponse("Inactive user.")
#         else:
#             return HttpResponseRedirect(settings.LOGIN_URL)
#     return render_to_response('login/login.html', {'redirect_to': redirect_to}, RequestContext(request))


def reset_password(request):
    return password_reset(request, template_name='login/password_reset_form.html',
                          email_template_name='login/password_reset_email.html',
                          subject_template_name='login/password_reset_subject.txt',
                          post_reset_redirect=reverse('reset_password_done'))


def reset_password_done(request):
    messages.info(request, "Email is sent.")
    messages.info(request, "Please, check your email box.")
    return HttpResponseRedirect('/home/', RequestContext(request))


def reset_password_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='login/password_reset_confirm.html', uidb64=uidb64,
                                  token=token, post_reset_redirect=reverse('login'))


def user_logout(request):
    redirect_to = request.GET.get('next', '/home/')
    logout(request)
    return HttpResponseRedirect(redirect_to, RequestContext(request))


def register(request):
    redirect_to = request.GET.get('next', '/home/')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.save()
            username = request.POST['username']
            password = request.POST['password']
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            messages.info(request, "Thanks for registration.")
            messages.info(request, "User '{}' is logged in.".format(username))
            return HttpResponseRedirect(redirect_to, RequestContext(request))
        else:
            print form.errors
    else:
        form = UserForm()

    return render_to_response('register/register.html', {'form': form, 'redirect_to': redirect_to}, RequestContext(request))


# def hours_ahead(request, offset):
#     hour_offset = int(offset)
#     next_time = datetime.datetime.now() + datetime.timedelta(hours=hour_offset)
#     return render_to_response("datetime/hours_ahead.html", locals())


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')
            send_mail(
            'Feedback from your site, topic: %s' % topic,
            message, sender,
            ['artyomsliusar@gmail.com']
            )
            return HttpResponseRedirect('thanks')
    else:
        form = ContactForm()
    return render_to_response('contact/contact.html', {'form': form}, RequestContext(request))


def thanks(request):
    return render_to_response('common/thanks.html')


# def show_posts():
#     form = PostForm()
#     return form


def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('thanks')
    else:
        form = PublisherForm()
    return render_to_response('books/add_publisher.html', {'form': form}, RequestContext(request))