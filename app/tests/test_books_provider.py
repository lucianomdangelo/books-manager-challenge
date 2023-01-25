from app.config import settings
from app.providers.books_provider import provide_book_by_isbn
import requests
from fastapi import HTTPException

import pytest

def test_provide_book_by_isbn_exception_ok(requests_mock):
    isbn = '1234'
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json= {'isbn': 'awesome-mock'})
    
    with pytest.raises(HTTPException) as exc_info:
        response = provide_book_by_isbn(isbn)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Please check the ISBN. It's must be 10 or 13 digits length"

def test_provide_book_by_isbn_ok(requests_mock):
    isbn = '1234567890'
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json= {'isbn': 'awesome-mock'})

    response = provide_book_by_isbn(isbn)
    
    assert response == {'isbn': 'awesome-mock'}

def test_provide_book_by_isbn_not_found_ok(requests_mock):
    isbn = '1234567890'
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json={}, status_code=200)

    with pytest.raises(HTTPException) as exc_info:
        response = provide_book_by_isbn(isbn)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Book not found on the books provider"