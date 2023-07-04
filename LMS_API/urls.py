from django.urls import path, include
from .views import *

urlpatterns = [
    path('v1/book/create', booksCreate, name='api-books-create'),
    path('v1/book/read', booksRead, name='api-books-read'),
    path('v1/book/read/<int:book_id>', booksReadDetails, name='api-books-read-details'),
    path('v1/book/update/<int:book_id>', booksUpdate, name='api-books-update'),
    path('v1/book/delete/<int:book_id>', booksDelete, name='api-books-delete'),

    path('v1/author/create', authorCreate, name='api-author-create'),
    path('v1/author/read', authorRead, name='api-author-read'),
    path('v1/author/read/<int:author_id>', authorReadDetails, name='api-author-read-details'),
    path('v1/author/update/<int:author_id>', authorUpdate, name='api-author-update'),
    path('v1/author/delete/<int:author_id>', authorDelete, name='api-author-delete'),

    path('v1/author/books/register', authorBookAdd, name='api-author-book-add'),
    path('v1/author/books/unregister', authorBookRemove, name='api-author-book-remove'),

    path('v1/borrow-book', borrowBook, name='api-book-borrow'),
    path('v1/borrow-book/history', borrowBookHistory, name='api-book-borrow-history'),
    path('v1/borrow-book/history/<int:lend_id>', borrowBookHistoryDetails, name='api-book-borrow-history-details'),
    path('v1/return-book', returnBook, name='api-book-return'),
]
