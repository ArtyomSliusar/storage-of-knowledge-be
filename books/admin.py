from django.contrib import admin
from .models import Author, Publisher, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Publisher)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Book)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    list_filter = ('publisher', 'publication_date')
    ordering = ('-publication_date',)
    search_fields = ('title',)
