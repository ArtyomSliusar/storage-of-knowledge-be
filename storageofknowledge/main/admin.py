from django.contrib import admin
from main.models import *


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'subjects_list', 'user', 'private', 'date_created')
    search_fields = ('id', 'topic')
    filter_horizontal = ('subjects',)

    def subjects_list(self, obj):
        return " | ".join([subject.name for subject in obj.subjects.all()])


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subjects_list', 'user', 'private')
    search_fields = ('id', 'name')
    filter_horizontal = ('subjects',)

    def subjects_list(self, obj):
        return " | ".join([subject.name for subject in obj.subjects.all()])


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'user', 'date_created')
    search_fields = ('id', 'note')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'subjects_list', 'date_created')
    search_fields = ('id', 'title')
    filter_horizontal = ('subjects',)

    def subjects_list(self, obj):
        return " | ".join([subject.name for subject in obj.subjects.all()])


@admin.register(Backlog)
class BacklogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    search_fields = ('id', 'title')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'state', 'deadline', 'notify_before_deadline', 'date_created')
    search_fields = ('id', 'title')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'subjects_list', 'date_created')
    search_fields = ('id', 'title')
    filter_horizontal = ('subjects',)

    def subjects_list(self, obj):
        return " | ".join([subject.name for subject in obj.subjects.all()])


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
