from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Subjects(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Notes(models.Model):
    topic = models.CharField(max_length=100)
    body = RichTextField()
    subject = models.ForeignKey(Subjects)
    user = models.ForeignKey(User)
    private = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

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
    user = models.ForeignKey(User)
    type = models.ForeignKey(TypeTable)
    date = models.DateTimeField(auto_now_add=True)

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
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=2000)
    resource_id = models.IntegerField()
    type = models.ForeignKey(TypeTable)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    time_zone = models.CharField(max_length=50)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
