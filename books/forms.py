__author__ = 'Artem'

from django import forms
from models import Publisher, Post
from django.forms import ModelForm
from django.contrib.auth.models import User


TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
    )


class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea(), initial="Replace with your feedback")
    sender = forms.EmailField(required=False, initial='user@example.com')

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message


class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address', 'city']


class PostForm(ModelForm):
    #subject = forms.ModelChoiceField(queryset=Post.objects.only("subject"))
    #topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    #text_to_search = forms.CharField(label='Search for:', max_length=100)

    class Meta:
        model = Post
        fields = ['subject', 'topic']


class UserForm(ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'User with this email address is already registered.')
        return email