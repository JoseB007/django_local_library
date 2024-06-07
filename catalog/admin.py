from django.contrib import admin
from .models import Book, BookInstance, Author, Genre

# Register your models here.

# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)


# class AuthorInstanceInline(admin.TabularInline):
#     model = Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # inlines = [AuthorInstanceInline]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Detalles', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Disponibilidad', {
            'fields': ('status', 'due_back')
        }),
    )


admin.site.register(Author, AuthorAdmin)