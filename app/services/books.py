from fastapi import HTTPException

from app.providers.books_provider import provide_book_by_isbn

from app.database.crud.books import books_crud
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException

def get_book_from_db(isbn: str):
    book_in_db = books_crud.get_by_isbn(isbn)
    if not book_in_db:
        raise HTTPException(status_code=404, detail="No book were found on the system")
    return book_in_db

def get_all_books_from_db():
    all_book_in_db = books_crud.get_all_books()
    if not all_book_in_db:
        raise HTTPException(status_code=404, detail="No books were found on the system")
    return all_book_in_db

def create_book_in_db(isbn: str):
    ## get info from provider    
    book_provided = provide_book_by_isbn(isbn)
    if book_provided == "{}":
        print("Book from provider is empty") 
        raise HTTPException(status_code=400, detail="Book not found on the books provider")
    
    ## create
    try:
        book_created = books_crud.create(isbn, str(book_provided))
    except AlreadyExistsOnDBException as error:
        raise HTTPException(status_code=409, detail="The ISBN it's already exist on the system")

    return book_created

def update_book_in_db(isbn: str):
    ## get info from provider    
    book_provided = provide_book_by_isbn(isbn)
    if book_provided == "{}":
        print("Book from provider is empty") 
        raise HTTPException(status_code=400, detail="Book not found on the books provider")

    ## update in db
    try: 
        book_updated = books_crud.update(isbn, str(book_provided))
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=409, detail="The ISBN it's does not exists on the system")

    return book_updated

def delete_book_in_db(isbn: str):
    try: 
        book_deleted = books_crud.delete(isbn)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=404, detail="The ISBN it's does not exists on the system")

    return book_deleted