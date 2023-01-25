from app.tests.conftest import app
from app.database.crud.books import books_crud
from fastapi.testclient import TestClient
from app.config import settings

### GET /books/{isbn}
def test_get_books_ok(get_book, client):
    isbn='9780140328721'
    response = client.get("/books/{isbn}".format(isbn=isbn))
    
    assert response.json()['isbn'] == isbn
    assert response.status_code == 200

def test_get_books_not_found(client):
    isbn='9780140328721'
    response = client.get("/books/{isbn}".format(isbn=isbn))
    
    assert response.status_code == 404
    assert response.text == '{"detail":"No book were found on the system"}'


### POST /books
def test_post_books_ok(client, requests_mock):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json=json_body, status_code=200)

    response = client.post("/books", json={'isbn': isbn,'info': info})
    
    print(response.json())

    assert response.status_code == 200
    assert response.json()['isbn'] == isbn
    assert response.json()['info'] == str({'isbn': isbn,'info': info})

def test_post_books_not_found_on_provider(client, requests_mock):
    isbn='9780140328720'
    info='info'

    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json={}, status_code=200)

    response = client.post("/books", json={'isbn': isbn,'info': info})
    
    assert response.status_code == 404
    assert response.json()['detail'] == 'Book not found on the books provider'

def test_post_books_already_exists(get_book, client, requests_mock):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json=json_body, status_code=200)

    response = client.post("/books", json={'isbn': isbn,'info': info})
    print(response.json())
    
    assert response.status_code == 409
    assert response.text == '{"detail":"The ISBN it\'s already exist on the system"}'

def test_post_books_missing_parameter(client, requests_mock):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json=json_body, status_code=200)

    response = client.post("/books", json={})
    print(response.json())

    assert response.status_code == 422
    assert response.json()['detail'] == 'Missing parameter "isbn" on request body or its imcomplete'


### PUT /books/{isbn}
def test_put_books_ok(get_book, client, requests_mock):
    isbn='9780140328721'
    info='info'
    json_body = {'isbn': isbn,'info': info}
    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json=json_body, status_code=200)

    response = client.put("/books/{isbn}".format(isbn=isbn), json={'isbn': isbn,'info': info})
    
    print(response.json())

    assert response.status_code == 200
    assert response.json()['isbn'] == isbn
    assert response.json()['info'] == str({'isbn': isbn,'info': info})

def test_put_books_not_found_on_provider(client, requests_mock):
    isbn='9780140328720'
    info='info'

    requests_mock.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn), json={}, status_code=200)

    response = client.put("/books/{isbn}".format(isbn=isbn), json={'isbn': isbn,'info': info})
    
    assert response.status_code == 404
    assert response.json()['detail'] == 'Book not found on the books provider'

### DELETE /books/{isbn}
def test_delete_books_ok(get_book, client):
    isbn='9780140328721'
    response = client.delete("/books/{isbn}".format(isbn=isbn))
    
    assert response.json()['isbn'] == isbn
    assert response.status_code == 200

def test_delete_books_not_found(client):
    isbn='9780140328721'
    response = client.delete("/books/{isbn}".format(isbn=isbn))
    print(response.json())
    
    assert response.status_code == 404
    assert response.json()['detail'] == "The ISBN it's does not exists on the system"