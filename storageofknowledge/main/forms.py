# from django.contrib.auth import get_user_model
# from django import forms
# from .models import Note, Subject
# from django.forms import ModelForm
# from django.forms import modelform_factory
# from django.core.validators import URLValidator
# from django.contrib.auth.forms import UserCreationForm
#
#
# TOPIC_CHOICES = (
#     ('general', 'General enquiry'),
#     ('bug', 'Bug report'),
#     ('suggestion', 'Suggestion'),
#     )
#
#
# User = get_user_model()
#
#
# class ContactForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         sender = kwargs.pop('user_email')
#         super(ContactForm, self).__init__(*args, **kwargs)
#         self.fields['sender'].initial = sender
#
#     topic = forms.ChoiceField(choices=TOPIC_CHOICES)
#     message = forms.CharField(widget=forms.Textarea(
#         attrs={'placeholder': 'Leave your feedback here'}))
#     sender = forms.EmailField(required=False)
#
#
# NoteForm = modelform_factory(Note,
#                              fields=("subject", "topic", "body", "private"))
#
#
# class LinkForm(ModelForm):
#     link_name = forms.CharField(max_length=100)
#     link = forms.CharField(max_length=2000)
#
#     class Meta:
#         model = Links
#         fields = ("link_name", "link")
#
#     def clean_link(self):
#         url = self.cleaned_data.get('link')
#         validator = URLValidator()
#         try:
#             validator(url)
#         except forms.ValidationError:
#             raise forms.ValidationError(u'Incorrect url format')
#         return url
#
#
# class SearchNotesForm(forms.Form):
#     subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)
#     topic = forms.CharField(max_length=100, required=False)
#
#     def __init__(self, *args, **kwargs):
#         super(SearchNotesForm, self).__init__(*args, **kwargs)
#         self.fields['subject'].empty_label = "All"
#
#
# class UserForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         self.fields['username'].help_text = None
#         self.fields['password2'].help_text = None
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if email:
#             email_exists = User.objects.filter(email=email).exists()
#             if email_exists:
#                 raise forms.ValidationError(u'User with this email address is already registered.')
#         return email
#
#
# class EditUserForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#
#     def __init__(self, *args, **kwargs):
#         super(EditUserForm, self).__init__(*args, **kwargs)
#         self.fields['username'].help_text = None
#         self.fields['password2'].help_text = None
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         initial_username = self.initial['username']
#         email_exists = User.objects.filter(email=email).exclude(username=initial_username).exists()
#         if email and email_exists:
#             raise forms.ValidationError(u'User with this email address is already registered.')
#         return email
#
#     def save(self, commit=True):
#         user = super(EditUserForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
