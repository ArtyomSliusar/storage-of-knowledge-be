import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
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


class User(AbstractUser):
    """
    Custom User model with `email` required and other custom fields.
    """
    email = models.EmailField(_('email address'), unique=True)
    time_zone = models.CharField(max_length=50, validators=[validate_time_zone], blank=True)

    objects = UserManager()


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
    private = models.BooleanField(default=0)
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


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    link = models.URLField(max_length=2000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    private = models.BooleanField(default=0)
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


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    note = models.ForeignKey(Note, related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
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

# TODO: remove when not needed
# class Subjects(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
#
# class Notes(models.Model):
#     topic = models.CharField(max_length=100)
#     body = models.TextField()
#     subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     private = models.BooleanField(default=0)
#     date = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.topic
#
#     class Meta:
#         ordering = ["topic"]
#
#
# class TypeTable(models.Model):
#     type_name = models.CharField(max_length=100)
#
#
# class Links(models.Model):
#     link_name = models.CharField(max_length=100)
#     link = models.CharField(max_length=2000)
#     subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     type = models.ForeignKey(TypeTable, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.link
#
#     class Meta:
#         ordering = ["link_name"]
#
#
# class LikesDislikes(models.Model):
#     type = models.ForeignKey(TypeTable, on_delete=models.CASCADE)
#     resource_id = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     like = models.BooleanField(default=0)
#     dislike = models.BooleanField(default=0)
#
#
# class Comments(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=2000)
#     resource_id = models.IntegerField()
#     type = models.ForeignKey(TypeTable, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.comment
#
#
# class UserProfile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     time_zone = models.CharField(max_length=50)
