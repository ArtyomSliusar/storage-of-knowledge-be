from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Note(models.Model):
    topic = models.CharField(max_length=100)
    body = models.TextField()
    comment = models.CharField(max_length=5000)
    subject = models.ForeignKey(Subject)
    user = models.ForeignKey(User)
    private = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

    class Meta:
        ordering = ["topic"]


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

