from app.config import settings

from fastapi import HTTPException

from app.services.comments import get_comment_from_db, get_all_comments_of_book_from_db, create_comment_of_book_in_db, update_comment_in_db, delete_comment_in_db

from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException

import pytest
from unittest.mock import MagicMock

### get_comment_from_db
def test_get_comment_from_db_ok(mocker):
    return_value = { "books_id": 1, "comment": "this book is awesome!", "id": 1 }
    mocker.patch('app.services.comments.comments_crud.get_comment_by_id', return_value=return_value)
    
    response = get_comment_from_db(1)

    assert response == return_value

def test_get_comment_from_db_on_exception(mocker):
    return_value = {}
    mocker.patch('app.services.comments.comments_crud.get_comment_by_id', return_value=return_value)

    with pytest.raises(HTTPException) as exc_info:
        response = get_comment_from_db(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Comment id does not correspond to a comment on the system"

### get_all_comments_of_book_from_db
def test_get_all_comments_of_book_from_db_ok(mocker):
    isbn = "1234567890"
    return_value = [{ "books_id": 1, "comment": "this book is awesome!", "id": 1 }]
    mocker.patch('app.services.comments.comments_crud.get_all_comments', return_value=return_value)

    response = get_all_comments_of_book_from_db(isbn)
    
    assert response == return_value

def test_get_all_comments_of_book_from_db_on_exception(mocker):
    isbn = "1234567890"
    return_value = []
    mocker.patch('app.services.comments.comments_crud.get_all_comments', return_value=return_value)

    with pytest.raises(HTTPException) as exc_info:
        response = get_all_comments_of_book_from_db(isbn)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No comments of this book were found on the system"

### create_comment_of_book
def test_create_comment_of_book_ok(mocker):
    isbn = "1234567890"
    comment = "This book is awesome!"
    return_value = { "books_id": 1, "comment": "this book is awesome!", "id": 1 }
    mocker.patch('app.services.comments.comments_crud.create', return_value=return_value)
    response = create_comment_of_book_in_db(isbn, comment)
    assert response == return_value

def test_create_comment_of_book_book_not_found(mocker):
    isbn = "1234567890"
    comment = "This book is awesome!"
    return_value = {}
    mocker.patch('app.services.comments.comments_crud.create', MagicMock(side_effect=NotFoundOnDBException()))

    with pytest.raises(HTTPException) as exc_info:
        response = create_comment_of_book_in_db(isbn, comment)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "The ISBN it's does not exists on the system"

### update_comment_in_db
def test_update_comment_in_db_ok(mocker):
    isbn = "1234567890"
    comment = "This book is awesome!"
    comment_id = "1"
    return_value = { "books_id": 1, "comment": "this book is awesome!", "id": 1 }
    mocker.patch('app.services.comments.comments_crud.update', return_value=return_value)
    response = update_comment_in_db(isbn, comment_id, comment)
    assert response == return_value

def test_update_comment_in_db_book_not_found(mocker):
    isbn = "1234567890"
    comment = "This book is awesome!"
    comment_id = "1"
    return_value = {}
    mocker.patch('app.services.comments.comments_crud.update', MagicMock(side_effect=NotFoundOnDBException()))

    with pytest.raises(HTTPException) as exc_info:
        response = update_comment_in_db(isbn, comment_id, comment)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Comment not found"

### delete_comment_in_db
def test_delete_comment_in_db_ok(mocker):
    comment_id = "1"
    return_value = { "books_id": 1, "comment": "this book is awesome!", "id": 1 }
    mocker.patch('app.services.comments.comments_crud.delete', return_value=return_value)
    response = delete_comment_in_db(comment_id)
    assert response == return_value


def test_delete_comment_in_db_book_not_found(mocker):
    isbn = "1234567890"
    comment = "This book is awesome!"
    comment_id = "1"
    return_value = {}
    mocker.patch('app.services.comments.comments_crud.delete', MagicMock(side_effect=NotFoundOnDBException()))

    with pytest.raises(HTTPException) as exc_info:
        response = delete_comment_in_db(comment_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Comment not found"