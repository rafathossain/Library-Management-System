import re

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from rest_framework.exceptions import ValidationError
from rest_framework import status
from LMS_Core.models import Books, Authors, BookLending
from datetime import datetime


class BooksSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class BooksInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    authors = serializers.SerializerMethodField('get_authors')

    def get_authors(self, instance: Books):
        return AuthorSerializer(instance.authors_set.all(), many=True).data

    class Meta:
        model = Books
        fields = ['id', 'title', 'publication_date', 'available', 'authors', 'created_at', 'updated_at']


class BooksBasicInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'title', 'publication_date']


class BooksUpdateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    publication_date = serializers.DateField(required=False)
    available = serializers.BooleanField(required=False)

    class Meta:
        model = Books
        fields = '__all__'


class AuthorSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ['id', 'name', 'created_at', 'updated_at']


class AuthorUpdateSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Authors
        fields = ['id', 'name', 'created_at', 'updated_at']


class AuthorInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    books = serializers.SerializerMethodField('get_books')

    def get_books(self, instance: Authors):
        return BooksSerializer(instance.books.all(), many=True).data

    class Meta:
        model = Authors
        fields = ['id', 'name', 'books', 'created_at', 'updated_at']


class AuthorBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)
    author_id = serializers.IntegerField(required=True)

    def validate_book_id(self, book_id) -> Books:
        """
        :param book_id:
        :return: Books
        """
        book = Books.objects.filter(id=book_id)
        if not book.exists():
            raise ValidationError('Book not found!', code=status.HTTP_404_NOT_FOUND)
        return book.last()

    def validate_author_id(self, author_id) -> Authors:
        """
        :param author_id:
        :return: Authors
        """
        author = Authors.objects.filter(id=author_id)
        if not author.exists():
            raise ValidationError('Author not found!', code=status.HTTP_404_NOT_FOUND)
        return author.last()


class BookLendCreateSerializer(serializers.Serializer):
    book_ids = serializers.ListField(required=True)
    borrower = serializers.JSONField(required=True)
    borrow_date = serializers.DateField(required=True)
    due_date = serializers.DateField(required=True)

    def validate_book_ids(self, book_ids):
        """
        :param book_ids:
        :return:
        """
        if not Books.objects.filter(id__in=book_ids, available=True).exists():
            raise ValidationError('Some Books are not found/available for lending!', code=status.HTTP_404_NOT_FOUND)
        return book_ids

    def validate_borrower(self, borrower):
        """
        :param borrower:
        :return:
        """
        borrower_fields = ['name', 'mobile']
        fields_exist = all(field in borrower for field in borrower_fields)
        if not fields_exist:
            raise ValidationError(f'Borrower information missing. Required fields are: {", ".join(borrower_fields)}', code=status.HTTP_400_BAD_REQUEST)
        blank_fields = [field for field in borrower_fields if not borrower.get(field)]
        if blank_fields:
            raise ValidationError(f'Borrower information fields can not be blank. Required fields are: {", ".join(borrower_fields)}', code=status.HTTP_400_BAD_REQUEST)
        return borrower

    def validate_due_date(self, due_date):
        """
        :param due_date:
        :return:
        """
        if due_date < datetime.today().astimezone().date():
            raise ValidationError("Due date can not be any dates before today.", code=status.HTTP_400_BAD_REQUEST)
        return due_date

    def validate_borrow_date(self, borrow_date):
        """
        :param borrow_date:
        :return:
        """
        if borrow_date > datetime.today().astimezone().date():
            raise ValidationError("Borrow date can not be any future dates.", code=status.HTTP_400_BAD_REQUEST)
        return borrow_date


class BookLendSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = BookLending
        fields = ['id', 'borrower', 'borrow_date', 'due_date', 'book_returned', 'return_date']


class BookLendInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    book = serializers.SerializerMethodField('get_book')

    def get_book(self, instance: BookLending):
        return BooksBasicInfoSerializer(instance.book.all(), many=True).data

    class Meta:
        model = BookLending
        fields = ['id', 'borrower', 'book', 'borrow_date', 'due_date', 'book_returned', 'return_date']


class BookLendReturnSerializer(serializers.Serializer):
    lend_id = serializers.IntegerField(required=True)
    return_date = serializers.DateField(required=True)

    def validate_lend_id(self, lend_id):
        lend_object = BookLending.objects.filter(id=lend_id, book_returned=False)
        if not lend_object.exists():
            raise ValidationError("No lending details found. Either the ID is invalid or book has been returned.", code=status.HTTP_404_NOT_FOUND)
        return lend_object.last()
