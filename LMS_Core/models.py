from django.db import models


class Books(models.Model):
    """
    Books model to manage the books in a Library
    """
    title = models.CharField(max_length=255, verbose_name='Book Title')
    publication_date = models.DateField()
    available = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Books'
        verbose_name_plural = 'Books'


class Authors(models.Model):
    """
    List of authors with their associated books
    """
    name = models.CharField(max_length=200, verbose_name='Author Name')
    books = models.ManyToManyField(Books, blank=True, verbose_name='Books of the Author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Authors'
        verbose_name_plural = 'Authors'


class BookLending(models.Model):
    """
    Manage the borrowing and return of a book
    """
    book = models.ManyToManyField(Books, verbose_name='Borrowed Books')
    borrower = models.JSONField(verbose_name='Borrower Information')
    borrow_date = models.DateField(verbose_name='Borrow Date')
    due_date = models.DateField(verbose_name='Due Date')
    book_returned = models.BooleanField(default=False, blank=True)
    return_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Borrow Date: {self.borrow_date}, Due Date: {self.due_date}"

    class Meta:
        verbose_name = 'Book Lending History'
        verbose_name_plural = 'Book Lending History'
