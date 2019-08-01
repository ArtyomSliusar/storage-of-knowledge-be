from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    time_zone = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Subjects(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Notes(models.Model):
    topic = models.CharField(max_length=100)
    body = RichTextField()
    subject = models.ForeignKey(Subjects)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    private = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ["topic"]


class TypeTable(models.Model):
    type_name = models.CharField(max_length=100)


class Links(models.Model):
    link_name = models.CharField(max_length=100)
    link = models.CharField(max_length=2000)
    subject = models.ForeignKey(Subjects)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    type = models.ForeignKey(TypeTable)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link

    class Meta:
        ordering = ["link_name"]


class LikesDislikes(models.Model):
    type = models.ForeignKey(TypeTable)
    resource_id = models.IntegerField()
    user = models.ForeignKey(User)
    like = models.BooleanField(default=0)
    dislike = models.BooleanField(default=0)


class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.CharField(max_length=2000)
    resource_id = models.IntegerField()
    type = models.ForeignKey(TypeTable)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    time_zone = models.CharField(max_length=50)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
