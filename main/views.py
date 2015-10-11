from django.db.models import Q
from django.shortcuts import render_to_response
from books.models import Book
from books.forms import ContactForm, PublisherForm, UserForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages


def search(request):
    query = request.GET('q', '')
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


def get_home(request):
    return render_to_response("home/index.html", context_instance=RequestContext(request))


def show_options(request):
    return render_to_response("learn_options/learn_options.html")


# def current_datetime(request):
#     now = datetime.datetime.now()
#     return render_to_response("datetime/current_datetime.html", {'current_date': now})


def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    # if user is not None:
    #     if user.is_active:
    #         login(request, user)
    #         # Redirect to a success page.
    #     else:
    #         # Return a 'disabled account' error message
    #         ...
    # else:
    #     # Return an 'invalid login' error message.
    #     ...


def register(request):
    redirect_to = request.REQUEST.get('next', '')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.save()
            username = request.POST['username']
            password = request.POST['password']
            new_user = authenticate(username=username,
                                    password=password)
            login(request, new_user)
            messages.info(request, "Thanks for registration.")
            messages.info(request, "User '{}' is logged in.".format(username))
            return HttpResponseRedirect(redirect_to, RequestContext(request))
            #new_user.backend = 'django.contrib.auth.backends.ModelBackend'

            # redirect, or however you want to get to the main view
            #return render_to_response('home/index.html')
        else:
            print form.errors
    else:
        form = UserForm()

    return render_to_response('register/register.html', {'form': form}, RequestContext(request))







    # if request.method == 'POST':
    #     user_name = request.REQUEST.get('username', None)
    #     user_pass = request.REQUEST.get('password', None)
    #     user_mail = request.REQUEST.get('email', None)
    #
    #     # TODO: check if already existed
    #     if user_name and user_pass and user_mail:
    #         new_user = User.objects.register(user_name, user_mail, user_pass)
    #     #    if created:
    #     #       # user was created
    #     #       # set the password here
    #     #    else:
    #     #       # user was retrieved
    #     # else:
    #     #    # request was empty
    #         new_user.save()
    #     return render_to_response('home/index.html')
    # else:
    #     form = CreateUserForm()
    # return render_to_response('register/register.html', {'form': form}, RequestContext(request))


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
    return render_to_response('contact/register.html', {'form': form}, RequestContext(request))


def thanks(request):
    return render_to_response('common/thanks.html')


def add_publisher(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('thanks')
    else:
        form = PublisherForm()
    return render_to_response('books/add_publisher.html', {'form': form}, RequestContext(request))