from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from main.models import Subject, Note, Link, Comment, Book, Backlog, Goal, Course
from django.utils.translation import gettext_lazy as _


User = get_user_model()


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subjects_list', 'user', 'private', 'date_created')
    search_fields = ('id', 'title')
    filter_horizontal = ('subjects',)

    def subjects_list(self, obj):
        return " | ".join([subject.name for subject in obj.subjects.all()])


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subjects_list', 'user', 'private')
    search_fields = ('id', 'title')
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
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'time_zone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
