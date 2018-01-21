
# TODO: redo work with comments (new model)
# TODO: check if note exist before edit/delete/show ...


import json
import pytz
import django_wysiwyg
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render
from .models import Notes, Comments, TypeTable, Links, Subjects, LikesDislikes
from .forms import ContactForm, UserForm, SearchNotesForm, NoteForm, EditUserForm, LinkForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from operator import attrgetter


def search_notes(request):

    """ Function looks for notes depending on current user, specified subject, specified topic. It looks in both topic
     and body fields of note, then compares the results and leaves only unique notes. The final results from topic
     and body fields are separated on the page.
     NOTE: body search is temporary disabled. """

    # TODO: perform search in the body field using AJAX

    form = SearchNotesForm(request.GET, empty_permitted=True)
    topic_results = []
    body_results = []
    user = None
    type_id = TypeTable.objects.get(type_name='note_notes').id
    if form.is_valid():
        subject = request.GET.get('subject', '')
        topic = request.GET.get('topic', '')
        topic_qset = (Q(private=0))  # qset for note's topic
        # body_qset = (Q(private=0))  # qset for note's body

        if request.user.is_authenticated():
            user = User.objects.get(id=request.user.id)
            topic_qset.add(Q(user_id=user), Q.OR)
            # body_qset.add(Q(user_id=user), Q.OR)

        if subject:  # if subject was specified in request
            topic_qset.add(Q(subject=subject), Q.AND)
            # body_qset.add(Q(subject=subject), Q.AND)
        if topic:  # if topic was specified in request
            topic_qset.add(Q(topic__icontains=topic), Q.AND)
            # body_qset.add(Q(body__icontains=topic), Q.AND)
        else:
            body_qset = []  # if there was no topic specified, do not look in body

        topic_results = Notes.objects.filter(topic_qset).distinct()

        # if body_qset:
        #     body_results = Notes.objects.filter(body_qset).distinct()
        #     body_results = set(body_results) - set(topic_results)  # compare topic and body results and leave unique only

        topic_results = get_likes_dislikes(topic_results, type_id, user)

    return render(request, "note_options/note_options.html", {'form': form, "topic_results": topic_results,
                                                                 "body_results": body_results, "query": True,
                                                                 'user': user, 'type_id': type_id})


@login_required
def add_note(request):

    """ Function to add new note. """

    redirect_to = request.GET.get('next', '/home/')
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        cleaned_body = django_wysiwyg.clean_html(request.POST['body'])
        form = NoteForm(request.POST)
        form.instance.user = user
        form.instance.body = cleaned_body
        if form.is_valid():
            form.save()
            messages.info(request, "Your note was successfully saved.")
            return HttpResponseRedirect(redirect_to, RequestContext(request))
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form, 'redirect_to': redirect_to})


@login_required
def edit_note(request):

    """ Function to edit existing note. Checks user rights before editing. """

    note_id = request.GET.get('id', '')
    note = Notes.objects.get(id=note_id)
    error = ''
    user = User.objects.get(id=request.user.id)
    if note.user_id != user.id:  # additional check in case of cheating
        error = 'This note is private, only author can edit this note.'
    if request.method == 'POST':
        cleaned_body = django_wysiwyg.clean_html(request.POST['body'])
        form = NoteForm(request.POST, instance=note)
        form.instance.user = user
        form.instance.body = cleaned_body
        form.instance.date = timezone.now()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/show_note/?id={}'.format(note_id), RequestContext(request))
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form, 'note_id': note_id, 'error': error})


@login_required
def delete_note(request):

    """ Function to delete specified note and comments for note. Checks user rights before deleting. """

    options = False
    note_id = request.GET.get('id', '')
    note = Notes.objects.get(id=note_id)
    type_id = TypeTable.objects.get(type_name='note_notes')
    if note.user_id == request.user.id:  # check if current user is author of note
        Comments.objects.filter(type_id=type_id, resource_id=note_id).delete()
        LikesDislikes.objects.filter(type_id=type_id, resource_id=note_id).delete()
        Notes.objects.get(id=note_id).delete()
        return HttpResponseRedirect('/search_notes/', RequestContext(request))
    else:
        error = 'This note is private, only author can delete this note.'
        return render(request, 'notes/show_note.html', {'note': note, 'error': error, 'options': options})


def show_note(request):

    """ Function to find specified note in database, find comments for note, check user rights for note. """

    note_id = request.GET.get('id', '')
    options = False
    error = ''
    note = ''
    is_auth_user = False
    comments = []
    type_id = TypeTable.objects.get(type_name='note_notes').id
    if note_id == '':  # if there is no "id" attribute or it is empty
        error = 'Wrong note id.'
    else:
        try:
            note = Notes.objects.get(id=note_id)
            comments = Comments.objects.filter(type_id=type_id, resource_id=note_id).order_by('-date')
            user_id = None
            if request.user.is_authenticated():
                is_auth_user = True
                user_id = request.user.id
            if note.user_id == user_id:
                options = True  # allow user to edit/delete note
            if note.private == 1:
                if note.user_id != user_id:  # additional check in case of cheating
                    error = 'This note is private, only author can view this note.'
                    note = ''
        except ObjectDoesNotExist:
            error = 'Note not found.'
    return render(request, 'notes/show_note.html', {'note': note, 'error': error, 'options': options,
                                                       'is_auth_user': is_auth_user, 'type_id': type_id,
                                                       'comments': comments})


def add_comment(request):

    """ Function uses ajax requests to add comments. """

    if not request.user.is_authenticated():
        return HttpResponse(status=307)

    if request.is_ajax():
        resource_id = request.POST.get('r_id', '')
        type_id = request.POST.get('t_id', '')
        cleaned_comment = django_wysiwyg.clean_html(request.POST['comment'])
        date = timezone.now()  # UTC format to save in database
        mimetype = 'application/json'
        model = None

        type_name = TypeTable.objects.get(id=type_id).type_name
        if type_name == 'learn_links' or type_name == 'check_links':
            model = Links
        elif type_name == 'note_notes':
            model = Notes
        if model:
            model.objects.get(id=resource_id)

        Comments(user=request.user, comment=cleaned_comment, resource_id=resource_id, type_id=type_id, date=date).save()
        date = timezone.localtime(date).strftime('%b %d, %Y %H:%M:%S')  # timezone format to send in ajax request
        data = json.dumps({"username": request.user.username, "date": date})
        return HttpResponse(data, mimetype)


def get_home(request):
    return render(request, "home/home.html")


def learn_options(request):
    return render(request, "learn_options/learn_options.html")


def check_options(request):
    return render(request, "check_options/check_options.html")


def note_options(request):

    """ Function represents to user special form to search for notes. """

    form = SearchNotesForm()
    return render(request, "note_options/note_options.html", {'form': form})


def get_topics(request):

    """ Function uses ajax request to autocomplete user's topic query. It looks for all public and current
    user's topics, taking into account chosen subject. """

    if request.is_ajax():
        query = request.GET.get('term', '')
        qset = (Q(topic__icontains=query))
        if request.user.is_authenticated():
            user_id = request.user.id
        else:
            user_id = None
        extra_param = request.GET.get('subject', '')
        if extra_param:
            qset.add(Q(subject=extra_param), Q.AND)
        notes = Notes.objects.filter(qset, Q(private=0) | Q(user_id=user_id))[:20]
        results = []
        for note in notes:
            results.append(note.topic)
        data = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


def reset_password(request):
    return password_reset(request, template_name='login/password_reset_form.html',
                          email_template_name='login/password_reset_email.html',
                          subject_template_name='login/password_reset_subject.txt',
                          post_reset_redirect=reverse('reset_password_done'))


def reset_password_done(request):
    messages.info(request, "Email was sent.")
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

    """ Function to create user, it collects such data: user name, email, password. After saving user it logs user
    in and renders to timezone setting. """

    redirect_to = request.GET.get('next', '/home/')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            messages.info(request, "Thanks for registration.")
            messages.info(request, "User '{}' is logged in.".format(username))
            return render(request, 'timezone/timezone.html', {'timezones': pytz.common_timezones, 'redirect_to': redirect_to})
    else:
        form = UserForm()
    return render(request, 'register/register.html', {'form': form, 'redirect_to': redirect_to})


@login_required
def edit_profile(request):

    """ Function to edit user data: user name, email, password. After saving user changes it logs user in and renders
    to timezone setting. """

    redirect_to = request.GET.get('next', '/home/')
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            edited_user = authenticate(username=username, password=password)
            login(request, edited_user)
            messages.info(request, "User '{}' is logged in.".format(username))
            return render(request, 'timezone/timezone.html', {'timezones': pytz.common_timezones, 'redirect_to': redirect_to})
    else:
        form = EditUserForm(instance=request.user)
    return render(request, 'register/edit_profile.html', {'form': form, 'redirect_to': redirect_to})


@login_required
def set_user_timezone(request):

    """ Function to save user specified timezone to user profile. """

    redirect_to = request.GET.get('next', '/home/')
    if request.method == 'POST':
        user_profile = request.user.profile
        user_profile.time_zone = request.POST['timezone']
        user_profile.save()
        return HttpResponseRedirect(redirect_to, RequestContext(request))
    else:
        return render(request, 'timezone/timezone.html', {'timezones': pytz.common_timezones, 'redirect_to': redirect_to})


def contact(request):
    redirect_to = request.GET.get('next', '/home/')
    user_email = 'unknown_user@example.com'
    user_name = 'unknown'
    if request.user.is_authenticated():
        user_email = request.user.email
        user_name = request.user.username
    if request.method == 'POST':
        form = ContactForm(request.POST, user_email=user_email)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')
            send_mail('Feedback from your site | topic: "%s" | sender email: "%s" | sender name: "%s"' % (topic, sender, user_name), message, '',
                      ['artyomsliusar@gmail.com'])
            messages.info(request, "Email to administrator was sent.")
            return HttpResponseRedirect(redirect_to, RequestContext(request))
    else:
        form = ContactForm(user_email=user_email)
    return render(request, 'contact/contact.html', {'form': form, 'redirect_to': redirect_to})


def show_links(request, type, back_address):

    """  """

    user = None
    user_name = None
    subject = request.GET.get('subject', '')
    if subject:
        subject_id = Subjects.objects.get(name=subject).id
    else:
        subject_id = request.GET.get('s_id', '')
    type_id = TypeTable.objects.get(type_name=type).id
    links = Links.objects.filter(type_id=type_id, subject_id=subject_id)
    if request.user.is_authenticated():
        user = request.user
        user_name = user.username
    links = get_likes_dislikes(links, type_id, user)
    return render(request, 'links/show_links.html', {'links': links, 'user': user_name, 'subject_id': subject_id,
                                                         'type_id': type_id, 'back_address': back_address})


def get_likes_dislikes(resources, type_id, user):
    for resource in resources:
        likes_dislikes = LikesDislikes.objects.filter(type_id=type_id, resource_id=resource.id)
        likes = likes_dislikes.filter(like=1)
        dislikes = likes_dislikes.filter(dislike=1)
        if user:
            # TODO: optimize, if one pressed - skip another
            resource.like_pressed = [True for like in likes if user.id == like.user_id]
            resource.dislike_pressed = [True for dislike in dislikes if user.id == dislike.user_id]
        resource.likes = len(likes)
        resource.dislikes = len(dislikes)
    # TODO: optimize sorting, try to make sorting in 'for' loop above
    return sorted(resources, key=attrgetter('likes'), reverse=True)


def show_learn_links(request):

    """  """

    return show_links(request, 'learn_links', 'learn_options')


def show_check_links(request):

    """  """

    return show_links(request, 'check_links', 'check_options')


@login_required
def add_link(request):

    """  """

    redirect_to = request.GET.get('next', '/home/')
    subject_id = request.GET.get('s_id', '')
    type_id = request.GET.get('t_id', '')
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = LinkForm(request.POST)
        form.instance.user = user
        form.instance.subject = Subjects.objects.get(id=subject_id)
        form.instance.type = TypeTable.objects.get(id=type_id)
        if form.is_valid():
            form.save()
            messages.info(request, "Your link was successfully saved.")
            return HttpResponseRedirect(redirect_to+'?s_id={}'.format(subject_id), RequestContext(request))
    else:
        form = LinkForm()
    return render(request, 'links/add_link.html', {'form': form, 'redirect_to': redirect_to+'&s_id={0}&t_id={1}'.format(subject_id, type_id)})


def delete_link(request):

    """  """

    if not request.user.is_authenticated():
        return HttpResponse(status=307)

    if request.is_ajax():
        link_id = request.POST.get('l_id', '')
        type_id = request.POST.get('type_id', '')
        user_id = request.user.id
        link = Links.objects.get(id=link_id)
        if link.user_id == user_id:
            LikesDislikes.objects.filter(type_id=type_id, resource_id=link_id).delete()
            link.delete()
        else:
            return HttpResponse('rights', status=403)
        data = json.dumps({'res': True})
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


def like_dislike(request):

    """  """

    if not request.user.is_authenticated():
        return HttpResponse(status=307)

    res = {'dislike': 0, 'like': 0}
    if request.is_ajax():
        resource_id = request.GET.get('resource_id', '')
        action = request.GET.get('action', '')
        type_id = request.GET.get('type_id', '')
        user_id = request.user.id
        try:
            resource = LikesDislikes.objects.get(type_id=type_id, resource_id=resource_id, user_id=user_id)
        except ObjectDoesNotExist:
            if action == 'like':
                LikesDislikes(dislike=0, like=1, user_id=user_id, type_id=type_id, resource_id=resource_id).save()
                res = {'dislike': 0, 'like': 1}
            elif action == 'dislike':
                LikesDislikes(dislike=1, like=0, user_id=user_id, type_id=type_id, resource_id=resource_id).save()
                res = {'dislike': 1, 'like': 0}
        else:
            if not resource.like and not resource.dislike:
                if action == 'like':
                    resource.like = 1
                    res = {'dislike': 0, 'like': 1}
                elif action == 'dislike':
                    resource.dislike = 1
                    res = {'dislike': 1, 'like': 0}
                resource.save()
            elif resource.like and not resource.dislike:
                resource.like = 0
                res = {'dislike': 0, 'like': -1}
                if action == 'dislike':
                    resource.dislike = 1
                    res = {'dislike': 1, 'like': -1}
                resource.save()
            elif resource.dislike and not resource.like:
                resource.dislike = 0
                res = {'dislike': -1, 'like': 0}
                if action == 'like':
                    resource.like = 1
                    res = {'dislike': -1, 'like': 1}
                resource.save()
            else:
                return HttpResponse('condition', status=501)
        data = json.dumps(res)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
