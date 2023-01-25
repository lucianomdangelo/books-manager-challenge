from app.tests.conftest import app
from app.database.crud.comments import comments_crud
from fastapi.testclient import TestClient
from app.config import settings

### GET /books/{isbn}/comments
def test_get_comments_ok(get_book_and_comment, client):
    isbn='9780140328721'
    response = client.get("/books/{isbn}/comments".format(isbn=isbn))
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['comment'] == 'comment'

def test_get_comments_not_found(get_book, client):
    isbn='9780140328721'
    response = client.get("/books/{isbn}/comments".format(isbn=isbn))
    
    assert response.status_code == 404
    assert response.text == '{"detail":"No comments of this book were found on the system"}'

def test_get_comments_book_not_found(client):
    isbn='9780140328721'
    response = client.get("/books/{isbn}/comments".format(isbn=isbn))
    
    assert response.status_code == 404
    assert response.text == '{"detail":"No comments of this book were found on the system"}'


### POST /books/{isbn}/comments
def test_post_comments_ok(get_book, client):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}

    response = client.post("/books/{isbn}/comments".format(isbn=isbn), json={'comment': info})
    
    print(response.json())

    assert response.status_code == 200
    assert response.json()['comment'] == info

def test_post_comments_no_book(client):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}

    response = client.post("/books/{isbn}/comments".format(isbn=isbn), json={'comment': info})
    
    print(response.json())

    assert response.status_code == 409
    assert response.json()['detail'] == "The ISBN it's does not exists on the system"

def test_post_comments_missing_parameter(client):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}

    response = client.post("/books/{isbn}/comments".format(isbn=isbn), json={})
    print(response.json())

    assert response.status_code == 422
    assert response.json()['detail'] == "Missing parameter 'comment' on request body or its imcomplete"


### PUT /books/{isbn}/comments
def test_put_comments_ok(get_book_and_comment, client):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}

    response = client.put("/books/{isbn}/comments/{id}".format(isbn=isbn, id='1'), json={'comment': info})
    
    print(response.json())

    assert response.status_code == 200
    assert response.json()['comment'] == info

def test_put_comments_missing_parameters(get_book_and_comment, client):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}

    response = client.put("/books/{isbn}/comments/{id}".format(isbn=isbn, id='1'), json={})
    
    print(response.json())

    assert response.status_code == 422
    assert response.json()['detail'] == "Missing parameter 'comment' on request body or its imcomplete"

### DELETE /books/{isbn}/comments
def test_delete_comments_ok(get_book_and_comment, client):
    isbn='9780140328721'
    response = client.delete("/books/{isbn}/comments/{id}".format(isbn=isbn, id='1'))
    print(response.json())
    assert response.status_code == 200

def test_delete_comments_not_found(client):
    isbn='9780140328721'
    response = client.delete("/books/{isbn}/comments/{id}".format(isbn=isbn, id='1'))
    print(response.json())
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Comment not found"