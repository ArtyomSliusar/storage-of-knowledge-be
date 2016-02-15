
#TODO: 1) difference between "render_to_response" and "HttpResponseRedirect" and "render" and "reverse" ...
#TODO: 2) check is note exist before eidt/delete/show ...


import json
import pytz
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render_to_response
from my_storage.models import Note, CommentsForNote
from my_storage.forms import ContactForm, UserForm, SearchNotesForm, NoteForm, EditUserForm
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


def search_notes(request):

    """ Function looks for notes depending on current user, specified subject, specified topic. It looks in both topic
     and body fields of note, then compares the results and leaves only unique notes. The final results from topic
     and body fields are separated on the page. """

    form = SearchNotesForm(request.GET, empty_permitted=True)
    users_only = request.GET.get('users_only')  # only current user's notes
    topic_results = []
    body_results = []
    user = None
    options = False
    if form.is_valid():
        subject = request.GET.get('subject', '')
        topic = request.GET.get('topic', '')
        topic_qset = (Q(private=0))  # qset for note's topic
        body_qset = (Q(private=0))  # qset for note's body

        if request.user.is_authenticated():
            user = User.objects.get(id=request.user.id)
            topic_qset.add(Q(user_id=user), Q.OR)
            body_qset.add(Q(user_id=user), Q.OR)
            options = True  # displays users_only checkbox on page

        if subject:  # if subject was specified in request
            topic_qset.add(Q(subject=subject), Q.AND)
            body_qset.add(Q(subject=subject), Q.AND)
        if topic:  # if topic was specified in request
            topic_qset.add(Q(topic__icontains=topic), Q.AND)
            body_qset.add(Q(body__icontains=topic), Q.AND)
        else:
            body_qset = []  # if there was no topic specified, do not look in body

        topic_results = Note.objects.filter(topic_qset).distinct()

        if body_qset:
            body_results = Note.objects.filter(body_qset).distinct()
            body_results = set(body_results) - set(topic_results)  # compare topic and body results and leave unique only

        if users_only:  # if checkbox enabled, leave current user's notes only
            topic_results = topic_results.filter(user_id=user)
            body_results = [note for note in body_results if note.user_id == user.id]

    return render_to_response("note_options/note_options.html", {'form': form, "topic_results": topic_results,
                                                                 "body_results": body_results, "query": True,
                                                                 'options': options}, RequestContext(request))


@login_required
def add_note(request):

    """ Function to add new note. """

    redirect_to = request.GET.get('next', '/home/')
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = NoteForm(request.POST)
        form.instance.user = user
        if form.is_valid():
            form.save()
            messages.info(request, "Your note was successfully saved.")
            return HttpResponseRedirect(redirect_to, RequestContext(request))
    else:
        form = NoteForm()
    return render_to_response('notes/add_note.html', {'form': form, 'redirect_to': redirect_to}, RequestContext(request))


@login_required
def edit_note(request):

    """ Function to edit existing note. Checks user rights before editing. """

    note_id = request.GET.get('id', '')
    note = Note.objects.get(id=note_id)
    error = ''
    user = User.objects.get(id=request.user.id)
    if note.user_id != user.id:  # additional check in case of cheating
        error = 'This note is private, only author can edit this note.'
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        form.instance.user = user
        form.instance.date = timezone.now()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/show_note/?id={}'.format(note_id), RequestContext(request))
    else:
        form = NoteForm(instance=note)
    return render_to_response('notes/edit_note.html', {'form': form, 'note_id': note_id, 'error': error}, RequestContext(request))


@login_required
def delete_note(request):

    """ Function to delete specified note and comments for note. Checks user rights before deleting. """

    options = False
    note_id = request.GET.get('id', '')
    note = Note.objects.get(id=note_id)
    if note.user_id == request.user.id:  # check if current user is author of note
        CommentsForNote.objects.filter(note_id=note_id).delete()
        Note.objects.get(id=note_id).delete()
        return HttpResponseRedirect('/search_notes/', RequestContext(request))
    else:
        error = 'This note is private, only author can delete this note.'
        return render_to_response('notes/show_note.html', {'note': note, 'error': error, 'options': options}, RequestContext(request))


def show_note(request):

    """ Function to find specified note in database, find comments for note, check user rights for note. """

    note_id = request.GET.get('id', '')
    options = False
    error = ''
    note = ''
    is_auth_user = False
    comments = []
    if note_id == '':  # if there is no "id" attribute or it is empty
        error = 'Wrong note id.'
    else:
        try:
            note = Note.objects.get(id=note_id)
            comments = CommentsForNote.objects.filter(note_id=note_id).order_by('-date')
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
    return render_to_response('notes/show_note.html', {'note': note, 'error': error, 'options': options,
                                                       'is_auth_user': is_auth_user,
                                                       'comments': comments}, RequestContext(request))


@login_required
def add_comment(request):

    """ Function uses ajax requests to add comments to notes. """

    if request.is_ajax():
        comment = request.POST.get('comment', '')
        note_id = request.POST.get('note_id', '')
        date = timezone.now()  # UTC format to save in database
        CommentsForNote(user=request.user, comment=comment, note_id=note_id, date=date).save()
        date = timezone.localtime(date).strftime('%b %d, %Y %H:%M:%S')  # timezone format to send in ajax request
        data = json.dumps({"username": request.user.username, "date": date})
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


def get_home(request):
    return render_to_response("home/home.html", RequestContext(request))


def learn_options(request):
    return render_to_response("learn_options/learn_options.html", RequestContext(request))


def check_options(request):
    return render_to_response("check_options/check_options.html", RequestContext(request))


def note_options(request):

    """ Function represents to user special form to search for notes. """

    form = SearchNotesForm()
    return render_to_response("note_options/note_options.html", {'form': form}, RequestContext(request))


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
        notes = Note.objects.filter(qset, Q(private=0) | Q(user_id=user_id))[:20]
        results = []
        for note in notes:
            results.append(note.topic)
        data = json.dumps(results)
    else:
        data = 'fail'
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
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.save()
            username = request.POST['username']
            password = request.POST['password']
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            messages.info(request, "Thanks for registration.")
            messages.info(request, "User '{}' is logged in.".format(username))
            return render_to_response('timezone/timezone.html', {'timezones': pytz.common_timezones, 'redirect_to': redirect_to},
                                      RequestContext(request))
    else:
        form = UserForm()
    return render_to_response('register/register.html', {'form': form, 'redirect_to': redirect_to}, RequestContext(request))


@login_required
def edit_profile(request):

    """ Function to edit user data: user name, email, password. After saving user changes it logs user in and renders
    to timezone setting. """

    redirect_to = request.GET.get('next', '/home/')
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password']
            edited_user = authenticate(username=username, password=password)
            login(request, edited_user)
            messages.info(request, "User '{}' is logged in.".format(username))
            return render_to_response('timezone/timezone.html', {'timezones': pytz.common_timezones, 'redirect_to': redirect_to},
                                      RequestContext(request))
    else:
        form = EditUserForm(instance=request.user)
    return render_to_response('register/edit_profile.html', {'form': form, 'redirect_to': redirect_to}, RequestContext(request))


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
        return render_to_response('timezone/timezone.html', {'timezones': pytz.common_timezones, 'redirect_to': redirect_to},
                                  RequestContext(request))


def contact(request):
    redirect_to = request.GET.get('next', '/home/')
    user_email = 'unknown_user@example.com'
    if request.user.is_authenticated():
        user_email = request.user.email
    if request.method == 'POST':
        form = ContactForm(request.POST, user_email=user_email)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')
            send_mail('Feedback from your site, topic: "%s", sender: "%s"' % (topic, sender), message, '',
                      ['artyomsliusar@gmail.com'])
            messages.info(request, "Email to administrator was sent.")
            return HttpResponseRedirect(redirect_to, RequestContext(request))
    else:
        form = ContactForm(user_email=user_email)
    return render_to_response('contact/contact.html', {'form': form, 'redirect_to': redirect_to}, RequestContext(request))

