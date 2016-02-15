from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Note(models.Model):
    topic = models.CharField(max_length=100)
    body = models.TextField()
    subject = models.ForeignKey(Subject)
    user = models.ForeignKey(User)
    private = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ["topic"]


class CommentsForNote(models.Model):
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=5000)
    note = models.ForeignKey(Note)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    time_zone = models.CharField(max_length=50)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
