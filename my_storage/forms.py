__author__ = 'Artem Sliusar'


from django import forms
from models import Note
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import modelform_factory


TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
    )


class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('user_email')
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['sender'].initial = sender

    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea(), initial="Replace with your feedback")
    sender = forms.EmailField(required=False)


NoteForm = modelform_factory(Note, fields=("subject", "topic", "body", "private"))


class SearchNotesForm(ModelForm):

    class Meta:
        model = Note
        fields = ['subject', 'topic']

    def remove_error(self, field, message='This field is required.'):
        if message in self.errors[field][0] and len(self.errors[field]) == 1:
            del self.errors[field]

    def __init__(self, *args, **kwargs):
        super(SearchNotesForm, self).__init__(*args, **kwargs)
        self.fields['subject'].empty_label = "All"
        if self.errors:
            if 'subject' in self.errors:
                self.remove_error('subject')
            if 'topic' in self.errors:
                self.remove_error('topic')


class UserForm(ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            same_email_count = User.objects.filter(email=email).count()
            if same_email_count:
                raise forms.ValidationError(u'User with this email address is already registered.')
            return email


class EditUserForm(ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        initial_username = self.initial['username']
        same_email_count = User.objects.filter(email=email).exclude(username=initial_username).count()
        if email and same_email_count:
            raise forms.ValidationError(u'User with this email address is already registered.')
        return email

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user