from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import *
from LMS_Core.models import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist


@api_view(['POST'])
def booksCreate(request):
    """
    :param request: Fields required to create a book
    :return:
    """
    payload = request.data

    create_book_serializer = BooksSerializer(data=payload)

    if create_book_serializer.is_valid(raise_exception=True):
        create_book_serializer.save()
        return Response({
            'message': "Book has been created successfully.",
            'data': create_book_serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def booksRead(request):
    """
    :param request:
    :return: Return the paginated list of books
    """
    book_list = Books.objects.all().order_by('title')
    paginator = PageNumberPagination()
    paginator.page_size = request.GET.get('count', 10)
    result_page = paginator.paginate_queryset(book_list, request)
    serializer = BooksSerializer(result_page, many=True, context={'request': request})
    response = paginator.get_paginated_response(serializer.data)
    return Response({
        'message': "Book list received successfully.",
        'data': {
            'count': response.data.get('count'),
            'next': response.data.get('next'),
            'previous': response.data.get('previous'),
            'results': response.data.get('results')
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def booksReadDetails(request, book_id: int):
    """
    :param request:
    :param book_id: PK of the Book
    :return: Return the information of a single book
    """
    try:
        book_info = Books.objects.get(id=book_id)
        serializer = BooksInfoSerializer(book_info, many=False, context={'request': request})
        return Response({
            'message': "Book information received successfully.",
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            'message': f"No book found!",
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'message': e.__str__(),
            'data': {}
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def booksUpdate(request, book_id: int):
    """
    :param request:
    :param book_id: PK of the Book
    :return: the updated info of a book
    """
    try:
        book_instance = Books.objects.get(id=book_id)
    except ObjectDoesNotExist:
        return Response({
            'message': f"No book found!",
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)

    payload = request.data

    update_book_serializer = BooksUpdateSerializer(instance=book_instance, data=payload)

    if update_book_serializer.is_valid(raise_exception=True):
        update_book_serializer.save()
        return Response({
            'message': "Book has been updated successfully.",
            'data': update_book_serializer.data
        }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def booksDelete(request, book_id: int):
    """
    :param request: Delete a book object
    :param book_id: Pk of the book
    :return:
    """
    try:
        book_instance = Books.objects.get(id=book_id)
        book_instance.delete()
        return Response({
            'message': "Book has been deleted successfully.",
            'data': {}
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            'message': f"No book found!",
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def authorCreate(request):
    """
    :param request: Fields required to create an author
    :return:
    """
    payload = request.data

    create_author_serializer = AuthorSerializer(data=payload)

    if create_author_serializer.is_valid(raise_exception=True):
        create_author_serializer.save()
        return Response({
            'message': "Author has been created successfully.",
            'data': create_author_serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def authorRead(request):
    """
    :param request:
    :return: Return the paginated list of authors
    """
    author_list = Authors.objects.all().order_by('name')
    paginator = PageNumberPagination()
    paginator.page_size = request.GET.get('count', 10)
    result_page = paginator.paginate_queryset(author_list, request)
    serializer = AuthorSerializer(result_page, many=True, context={'request': request})
    response = paginator.get_paginated_response(serializer.data)
    return Response({
        'message': "Author list received successfully.",
        'data': {
            'count': response.data.get('count'),
            'next': response.data.get('next'),
            'previous': response.data.get('previous'),
            'results': response.data.get('results')
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def authorReadDetails(request, author_id: int):
    """
    :param request:
    :param author_id: PK of the author
    :return: Return the information of a single author with books
    """
    try:
        author_info = Authors.objects.get(id=author_id)
        serializer = AuthorInfoSerializer(author_info, many=False, context={'request': request})
        return Response({
            'message': "Author information received successfully.",
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            'message': f"No author found!",
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'message': e.__str__(),
            'data': {}
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def authorUpdate(request, author_id: int):
    """
    :param request:
    :param author_id: PK of the Author
    :return: the updated info of an author
    """
    try:
        author_instance = Authors.objects.get(id=author_id)
    except ObjectDoesNotExist:
        return Response({
            'message': f"No author found!",
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)

    payload = request.data

    update_author_serializer = AuthorUpdateSerializer(instance=author_instance, data=payload)

    if update_author_serializer.is_valid(raise_exception=True):
        update_author_serializer.save()
        return Response({
            'message': "Author has been updated successfully.",
            'data': update_author_serializer.data
        }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def authorDelete(request, author_id: int):
    """
    :param request: Delete an author object
    :param author_id: Pk of the author
    :return:
    """
    try:
        author_instance = Authors.objects.get(id=author_id)
        author_instance.delete()
        return Response({
            'message': "Author has been deleted successfully.",
            'data': {}
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            'message': f"No author found!",
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def authorBookAdd(request):
    """
    :param request: Add a book to an author
    :return:
    """
    payload = request.data

    assign_book_serializer = AuthorBookSerializer(data=payload)
    if assign_book_serializer.is_valid(raise_exception=True):
        book_instance = assign_book_serializer.validated_data.get('book_id')
        author_instance = assign_book_serializer.validated_data.get('author_id')
        if author_instance.books.filter(id=book_instance.id).exists():
            return Response({
                'message': 'This Book has already been registered to author.',
                'data': {}
            })
        else:
            author_instance.books.add(book_instance)
            return Response({
                'message': 'Book has been registered to author.',
                'data': {}
            })


@api_view(['POST'])
def authorBookRemove(request):
    """
    :param request: Remove a book from an author
    :return:
    """
    payload = request.data

    remove_book_serializer = AuthorBookSerializer(data=payload)
    if remove_book_serializer.is_valid(raise_exception=True):
        book_instance = remove_book_serializer.validated_data.get('book_id')
        author_instance = remove_book_serializer.validated_data.get('author_id')
        if author_instance.books.filter(id=book_instance.id).exists():
            author_instance.books.remove(book_instance)
            return Response({
                'message': 'This Book has been unregistered from author.',
                'data': {}
            })
        else:
            return Response({
                'message': 'This Book has not been registered to author.',
                'data': {}
            })


@api_view(['POST'])
def borrowBook(request):
    """
    :param request: Create a transaction for book borrowing
    :return:
    """
    payload = request.data

    borrow_book_serializer = BookLendCreateSerializer(data=payload)
    if borrow_book_serializer.is_valid(raise_exception=True):
        book_ids = borrow_book_serializer.validated_data.get('book_ids')
        borrower_information = borrow_book_serializer.validated_data.get('borrower')
        borrow_date = borrow_book_serializer.validated_data.get('borrow_date')
        due_date = borrow_book_serializer.validated_data.get('due_date')

        lend_object = BookLending.objects.create(
            borrower=borrower_information,
            borrow_date=borrow_date,
            due_date=due_date
        )
        for book in book_ids:
            book_instance = Books.objects.get(id=book)
            lend_object.book.add(book_instance)
            book_instance.available = False
            book_instance.save()

        return Response({
            'message': 'Books have been lend successfully.',
            'data': BookLendInfoSerializer(lend_object).data
        })


@api_view(['GET'])
def borrowBookHistory(request):
    """
    :param request:
    :return: History of borrowed books
    """
    lend_list = BookLending.objects.all().order_by('borrow_date')
    paginator = PageNumberPagination()
    paginator.page_size = request.GET.get('count', 10)
    result_page = paginator.paginate_queryset(lend_list, request)
    serializer = BookLendSerializer(result_page, many=True, context={'request': request})
    response = paginator.get_paginated_response(serializer.data)
    return Response({
        'message': "Lend list received successfully.",
        'data': {
            'count': response.data.get('count'),
            'next': response.data.get('next'),
            'previous': response.data.get('previous'),
            'results': response.data.get('results')
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def borrowBookHistoryDetails(request, lend_id: int):
    """
    :param request:
    :param lend_id: ID of the BookLending
    :return: History of borrowed books
    """
    try:
        lend_info = BookLending.objects.get(id=lend_id)
        serializer = BookLendInfoSerializer(lend_info, many=False, context={'request': request})
        return Response({
            'message': "Lending information received successfully.",
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            'message': f"No data found!",
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'message': e.__str__(),
            'data': {}
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def returnBook(request):
    """
    :param request: Mark a transaction as returned
    :return:
    """
    payload = request.data

    return_book_serializer = BookLendReturnSerializer(data=payload)
    if return_book_serializer.is_valid(raise_exception=True):
        lend_object = return_book_serializer.validated_data.get('lend_id')

        for book in lend_object.book.all():
            book.available = True
            book.save()

        lend_object.return_date = return_book_serializer.validated_data.get('return_date')
        lend_object.book_returned = True
        lend_object.save()

        return Response({
            'message': 'Books have been returned successfully.',
            'data': BookLendInfoSerializer(lend_object).data
        })
