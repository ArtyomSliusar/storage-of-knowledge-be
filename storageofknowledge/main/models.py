import uuid
from enum import Enum
from typing import Optional
from django.template import loader
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from main.utils import get_random_key
from main.validators import validate_time_zone
from django.utils.translation import gettext_lazy as _


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted', email='deleted@storageofknowledge.com')[0]


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def get_by_username_or_email(self, value: str) -> Optional["User"]:
        return self.filter(Q(username=value) | Q(email=value)).first()


class User(AbstractUser):
    """
    Custom User model with `email` required and other custom fields.
    """
    email = models.EmailField(_('email address'), unique=True)
    time_zone = models.CharField(max_length=50, validators=[validate_time_zone], blank=True)

    objects = UserManager()

    @property
    def available_notes(self):
        return Note.objects.filter(Q(user=self, private=True) | Q(private=False))

    @property
    def available_links(self):
        return Link.objects.filter(Q(user=self, private=True) | Q(private=False))

    def activate(self, confirmation_key: str) -> bool:
        try:
            confirmation = self.confirmations.get(type=UserConfirmationType.ACTIVATION.name)
            self.is_active = True
            confirmation.confirm_user_update(confirmation_key)
        except (UserConfirmation.DoesNotExist, AssertionError):
            return False
        else:
            return True

    def reset_password(self, new_password, confirmation_key: str) -> bool:
        try:
            confirmation = self.confirmations.get(type=UserConfirmationType.PASSWORD_RESET.name)
            self.set_password(new_password)
            confirmation.confirm_user_update(confirmation_key)
        except (UserConfirmation.DoesNotExist, AssertionError):
            return False
        else:
            return True

    def send_confirmation(self, confirmation_type: "UserConfirmationType"):
        confirmation = UserConfirmation.objects.create_confirmation(self, confirmation_type.name)
        values = {
            'lifetime': int(settings.USER_CONFIRMATION_LIFETIME_HOURS),
            'secret': confirmation.secret_key
        }
        subject = confirmation_type.get_email_subject()
        message = confirmation_type.get_email_message(**values)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])


class UserConfirmationType(Enum):
    ACTIVATION = {
        'subject': "Email confirmation",
        'template': 'user_activation.txt'
    }
    PASSWORD_RESET = {
        'subject': "Password reset confirmation",
        'template': 'user_password_reset.txt'
    }

    @classmethod
    def choices(cls):
        return tuple((i.name, i.name.lower()) for i in cls)

    def get_email_subject(self, *args, **kwargs):
        return self.value['subject']

    def get_email_message(self, *args, **kwargs):
        return loader.render_to_string(
            'emails/{}'.format(self.value['template']),
            kwargs
        )


class UserConfirmationManager(models.Manager):

    def create_confirmation(self, user: User, confirmation_type: str) -> "UserConfirmation":
        confirmation, created = self.get_or_create(user=user, type=confirmation_type)
        if created is False:
            # just update secret key and timestamp
            confirmation.secret_key = get_random_key()
            confirmation.save()
        return confirmation


class UserConfirmation(models.Model):
    """For email and reset password confirmations"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='confirmations')
    secret_key = models.CharField(max_length=255, default=get_random_key)
    type = models.CharField(max_length=255, choices=UserConfirmationType.choices())
    date_created = models.DateTimeField(auto_now=True)
    objects = UserConfirmationManager()

    class Meta:
        db_table = "user_confirmation"
        unique_together = (
            ('user', 'type'),
        )

    def confirm_user_update(self, confirmation_key: str):
        assert self.secret_key == confirmation_key
        assert timezone.now() < self.date_created + timezone.timedelta(hours=settings.USER_CONFIRMATION_LIFETIME_HOURS)
        with transaction.atomic():
            self.user.save()
            self.delete()


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    body = models.TextField()
    subjects = models.ManyToManyField(Subject)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        unique_together = (
            ('title', 'user'),
        )

    def subjects_to_string(self):
        subjects_list = list(self.subjects.values_list('name', flat=True))
        return ' '.join(subjects_list)

    @property
    def str_id(self):
        return str(self.id)


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=2000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    private = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        unique_together = (
            ('title', 'user'),
        )

    def subjects_to_string(self):
        subjects_list = list(self.subjects.values_list('name', flat=True))
        return ' '.join(subjects_list)

    @property
    def str_id(self):
        return str(self.id)


class NoteLike(models.Model):
    note = models.ForeignKey(Note, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = "note_like"
        unique_together = (
            ('note', 'user'),
        )


class LinkLike(models.Model):
    link = models.ForeignKey(Link, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = "link_like"
        unique_together = (
            ('link', 'user'),
        )


class NoteComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="reply_set")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    note = models.ForeignKey(Note, related_name='comments', on_delete=models.CASCADE)
    body = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body

    class Meta:
        db_table = "note_comment"
        ordering = ["date_created"]


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        unique_together = (
            ('title', 'user', 'author'),
        )


class Backlog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["date"]
        unique_together = (
            ('title', 'user'),
        )


class Goal(models.Model):

    NOT_STARTED = 'NS'
    IN_PROGRESS = 'IP'
    DONE = 'DN'

    STATE_CHOICES = (
        (NOT_STARTED, 'not started'),
        (IN_PROGRESS, 'in progress'),
        (DONE, 'done'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        default=NOT_STARTED,
    )
    deadline = models.DateField()
    notify_before_deadline = models.SmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["state"]
        unique_together = (
            ('title', 'user'),
        )


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=2000)
    subjects = models.ManyToManyField(Subject)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        unique_together = (
            ('title', 'user'),
        )
