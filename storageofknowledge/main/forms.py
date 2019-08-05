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
#
#
# class UserCreationForm(BaseUserCreationForm):
#
#     class Meta(BaseUserCreationForm.Meta):
#         fields = ("username", "email")
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         validate_email(email)
#         return email
#
#
# class UserChangeForm(BaseUserChangeForm):
#
#     class Meta(BaseUserChangeForm.Meta):
#         fields = '__all__'
#
#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         username = cleaned_data.get('username')
#         validate_email(email, exclude_username=username)
#         return cleaned_data
