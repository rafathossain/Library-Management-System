from django.contrib import admin
from .models import *


class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_date', 'available']


class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['name']


class BookLendingAdmin(admin.ModelAdmin):
    list_display = ['borrower', 'borrow_date', 'due_date', 'book_returned', 'return_date']


admin.site.register(Books, BooksAdmin)
admin.site.register(Authors, AuthorsAdmin)
admin.site.register(BookLending, BookLendingAdmin)
