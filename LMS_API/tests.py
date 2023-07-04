import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient


class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.headers = {
            'Content-Type': 'application/json',
        }

    def test_create_book(self):
        url = reverse('api-books-create')
        data = {
            'title': 'Test Book',
            'publication_date': '2023-07-23',
            'available': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_books(self):
        url = reverse('api-books-read')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_book_details(self):
        book_id = 64648
        url = reverse('api-books-read-details', args=[book_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('api-books-create')
        data = {
            'title': 'Test Book',
            'publication_date': '2023-07-23',
            'available': True
        }
        response = self.client.post(url, data)
        book_id = response.data.get('data', {}).get('id')
        url = reverse('api-books-read-details', args=[book_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        url = reverse('api-books-create')
        data = {
            'title': 'Test Book',
            'publication_date': '2023-07-23',
            'available': True
        }
        response = self.client.post(url, data)
        book_id = response.data.get('data', {}).get('id')
        url = reverse('api-books-update', args=[book_id])
        data = {
            'title': 'Updated Book Title'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        url = reverse('api-books-create')
        data = {
            'title': 'Test Book',
            'publication_date': '2023-07-23',
            'available': True
        }
        response = self.client.post(url, data)
        book_id = response.data.get('data', {}).get('id')
        url = reverse('api-books-delete', args=[book_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_author(self):
        url = reverse('api-author-create')
        data = {
            'name': 'Rafat Doe'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_authors(self):
        url = reverse('api-author-read')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_author_details(self):
        author_id = 4556489
        url = reverse('api-author-read-details', args=[author_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('api-author-create')
        data = {
            'name': 'Rafat Doe'
        }
        response = self.client.post(url, data=data)
        author_id = response.data.get('data', {}).get('id')
        url = reverse('api-author-read-details', args=[author_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_author(self):
        url = reverse('api-author-create')
        data = {
            'name': 'Rafat Doe'
        }
        response = self.client.post(url, data=data)
        author_id = response.data.get('data', {}).get('id')
        url = reverse('api-author-update', args=[author_id])
        data = {
            'name': 'Updated Rafat'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_author(self):
        url = reverse('api-author-create')
        data = {
            'name': 'Rafat Doe'
        }
        response = self.client.post(url, data=data)
        author_id = response.data.get('data', {}).get('id')
        url = reverse('api-author-delete', args=[author_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_unregister_author_book(self):
        url = reverse('api-books-create')
        data = {
            'title': 'Test Book',
            'publication_date': '2023-07-23',
            'available': True
        }
        response = self.client.post(url, data)
        book_id = response.data.get('data', {}).get('id')

        url = reverse('api-author-create')
        data = {
            'name': 'Rafat Doe'
        }
        response = self.client.post(url, data=data)
        author_id = response.data.get('data', {}).get('id')

        url = reverse('api-author-book-add')
        data = {
            'author_id': author_id,
            'book_id': book_id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('api-author-book-remove')
        data = {
            'author_id': author_id,
            'book_id': book_id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrow_book(self):
        url = reverse('api-books-create')
        data = {
            'title': 'Test Book',
            'publication_date': '2023-07-23',
            'available': True
        }
        response = self.client.post(url, data)
        book_id = response.data.get('data', {}).get('id')

        url = reverse('api-book-borrow')
        data = {
            "book_ids": [book_id],
            "borrower": {
                "name": "Rafat"
            },
            "borrow_date": "2023-07-04",
            "due_date": "2025-05-08"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('api-book-borrow')
        data = {
            "book_ids": [book_id],
            "borrower": {
                "name": "Rafat",
                "mobile": ""
            },
            "borrow_date": "2023-07-04",
            "due_date": "2025-05-08"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('api-book-borrow')
        data = {
            "book_ids": [book_id],
            "borrower": {
                "name": "Rafat",
                "mobile": ""
            },
            "borrow_date": "2024-01-04",
            "due_date": "2025-05-08"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('api-book-borrow')
        data = {
            "book_ids": [book_id],
            "borrower": {
                "name": "Rafat",
                "mobile": ""
            },
            "borrow_date": "2023-07-01",
            "due_date": "2022-05-08"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse('api-book-borrow')
        data = {
            "book_ids": [book_id],
            "borrower": {
                "name": "Rafat",
                "mobile": "01704005054"
            },
            "borrow_date": "2023-07-04",
            "due_date": "2025-05-08"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrow_book_history(self):
        url = reverse('api-book-borrow-history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrow_book_history_details(self):
        url = reverse('api-books-create')
        data = {
            'title': 'Test Book',
            'publication_date': '2023-07-23',
            'available': True
        }
        response = self.client.post(url, data)
        book_id = response.data.get('data', {}).get('id')

        url = reverse('api-book-borrow')
        data = {
            "book_ids": [book_id],
            "borrower": {
                "name": "Rafat",
                "mobile": "01704005054"
            },
            "borrow_date": "2023-07-04",
            "due_date": "2025-05-08"
        }
        response = self.client.post(url, data=data)
        lend_id = response.data.get('data', {}).get('id')
        url = reverse('api-book-borrow-history-details', args=[lend_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        lend_id = 2342342
        url = reverse('api-book-borrow-history-details', args=[lend_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_return_book(self):
        url = reverse('api-books-create')
        data = {
            'title': 'Test Book',
            'publication_date': '2023-07-23',
            'available': True
        }
        response = self.client.post(url, data)
        book_id = response.data.get('data', {}).get('id')

        url = reverse('api-book-borrow')
        data = {
            "book_ids": [book_id],
            "borrower": {
                "name": "Rafat",
                "mobile": "01704005054"
            },
            "borrow_date": "2023-07-04",
            "due_date": "2025-05-08"
        }
        response = self.client.post(url, data=data)
        lend_id = response.data.get('data', {}).get('id')
        url = reverse('api-book-return')
        data = {
            "lend_id": lend_id,
            "return_date": "2023-05-23"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
