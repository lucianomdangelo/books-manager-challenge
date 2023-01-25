from app.config import settings

from fastapi import HTTPException

from app.services.books import get_book_from_db, get_all_books_from_db, create_book_in_db, update_book_in_db, delete_book_in_db

import pytest
from unittest.mock import MagicMock


#### get_book_from_db
def test_get_book_from_db_exception(mocker):
    isbn = '1234567890'
    mocker.patch('app.services.books.books_crud.get_by_isbn', return_value={})
    
    with pytest.raises(HTTPException) as exc_info:
        response = get_book_from_db(isbn)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No book were found on the system"

def test_get_book_from_db_ok(mocker):
    isbn = '1234567890'
    return_value_from_db = {"isbn": "{isbn}", "info": "book-info", "id":1}
    mocker.patch('app.services.books.books_crud.get_by_isbn', return_value=return_value_from_db)

    response = get_book_from_db(isbn)
    
    assert response == return_value_from_db

#### get_all_books_from_db
def test_get_all_books_from_db_exception(mocker):
    mocker.patch('app.services.books.books_crud.get_all_books', return_value={})
    
    with pytest.raises(HTTPException) as exc_info:
        response = get_all_books_from_db()
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No books were found on the system"

def test_get_all_books_from_db_ok(mocker):
    return_value_from_db = [{"isbn": "1234567890", "info": "book-info", "id":1}, {"isbn": "1234567891", "info": "book-info", "id":2}]
    mocker.patch('app.services.books.books_crud.get_all_books', return_value=return_value_from_db)

    response = get_all_books_from_db()
    
    assert response == return_value_from_db


#### create_book_in_db
def test_create_book_in_db_dont_exist_on_provider(mocker):
    isbn = "1234567890"
    mocker.patch('app.services.books.provide_book_by_isbn', MagicMock(side_effect=HTTPException(status_code=404, detail="Book not found on the books provider")))
    mocker.patch('app.services.books.books_crud.create', return_value='')
    
    with pytest.raises(HTTPException) as exc_info:
        response = create_book_in_db(isbn)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Book not found on the books provider"

def test_create_book_in_db_dont_exist_on_database(mocker, requests_mock):
    return_value_from_db = {}
    isbn = "1234567890"
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json={'isbn': '1234567890'})
    mocker.patch('app.services.books.books_crud.create', MagicMock(side_effect=HTTPException(status_code=409, detail="The ISBN it's already exist on the system")))
    
    
    with pytest.raises(HTTPException) as exc_info:
        response = create_book_in_db(isbn)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "The ISBN it's already exist on the system"

def test_create_book_in_db_ok(mocker, requests_mock):
    return_value_from_db = [{"isbn": "1234567890", "info": "book-info", "id":1}, {"isbn": "1234567891", "info": "book-info", "id":2}]
    isbn = "1234567890"
    
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json={'isbn': '1234567890'})    
    mocker.patch('app.services.books.books_crud.create', return_value=return_value_from_db)

    response = create_book_in_db(isbn)
    
    assert response == return_value_from_db

#### update_book_in_db
def test_update_book_in_db_dont_exist_on_provider(mocker):
    isbn = "1234567890"
    mocker.patch('app.services.books.provide_book_by_isbn', MagicMock(side_effect=HTTPException(status_code=404, detail="Book not found on the books provider")))
    mocker.patch('app.services.books.books_crud.update', return_value='')
    
    with pytest.raises(HTTPException) as exc_info:
        response = update_book_in_db(isbn)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Book not found on the books provider"

def test_update_book_in_db_dont_exist_on_database(mocker, requests_mock):
    return_value_from_db = {}
    isbn = "1234567890"
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json={'isbn': '1234567890'})
    mocker.patch('app.services.books.books_crud.update', MagicMock(side_effect=HTTPException(status_code=409, detail="The ISBN it's already exist on the system")))
    
    with pytest.raises(HTTPException) as exc_info:
        response = update_book_in_db(isbn)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "The ISBN it's already exist on the system"

def test_update_book_in_db_ok(mocker, requests_mock):
    return_value_from_db = [{"isbn": "1234567890", "info": "book-info", "id":1}, {"isbn": "1234567891", "info": "book-info", "id":2}]
    isbn = "1234567890"    
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json={'isbn': '1234567890'})    
    mocker.patch('app.services.books.books_crud.update', return_value=return_value_from_db)

    response = update_book_in_db(isbn)
    
    assert response == return_value_from_db

### delete
def test_delete_book_in_db_dont_exist_on_database(mocker, requests_mock):
    return_value_from_db = {}
    isbn = "1234567890"
    mocker.patch('app.services.books.books_crud.delete', MagicMock(side_effect=HTTPException(status_code=409, detail="The ISBN it's does not exists on the system")))
    
    with pytest.raises(HTTPException) as exc_info:
        response = delete_book_in_db(isbn)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "The ISBN it's does not exists on the system"

def test_delete_book_in_db_ok(mocker):
    return_value_from_db = [{"isbn": "1234567890", "info": "book-info", "id":1}, {"isbn": "1234567891", "info": "book-info", "id":2}]
    isbn = "1234567890"    
    mocker.patch('app.services.books.books_crud.delete', return_value=return_value_from_db)

    response = delete_book_in_db(isbn)
    
    assert response == return_value_from_db