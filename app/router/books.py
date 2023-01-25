from fastapi import APIRouter, HTTPException, Request, Depends
from app.services import books as books_service

from sqlalchemy.orm import Session
from contextvars import ContextVar
from app.dependencies import get_db, db_session

from app.providers.books_provider import validate_isbn


router = APIRouter(prefix="/books", tags=["/books"])

@router.get("/{isbn}")
def get_book_info(isbn: str, db: Session = Depends(get_db)):
    if not validate_isbn(isbn):
        raise HTTPException(status_code=422, detail="the isbn must be a digit of 10 or 12 characters length")

    db_session.set(db)
    return books_service.get_book_from_db(isbn)

@router.get("/")
def get_all_books(db: Session = Depends(get_db)):
    db_session.set(db)
    return books_service.get_all_books_from_db()

@router.post("/")
async def create_book_db(request: Request, db: Session = Depends(get_db)):
    db_session.set(db)
    try:
        request_json = await request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameter \"isbn\" on request body or its imcomplete")

    if not (request_json and 'isbn' in request_json and request_json['isbn']):
        raise HTTPException(status_code=422, detail="Missing parameter \"isbn\" on request body or its imcomplete")
    isbn = request_json['isbn']

    return books_service.create_book_in_db(isbn)

@router.put("/{isbn}")
def update_book_db(isbn: str, db: Session = Depends(get_db)):
    if not validate_isbn(isbn):
        raise HTTPException(status_code=422, detail="the isbn must be a digit of 10 or 12 characters length")

    db_session.set(db)
    return books_service.update_book_in_db(isbn)

@router.delete("/{isbn}")
def delete_book_db(isbn: str, db: Session = Depends(get_db)):
    if not validate_isbn(isbn):
        raise HTTPException(status_code=422, detail="the isbn must be a digit of 10 or 12 characters length")

    db_session.set(db)
    return books_service.delete_book_in_db(isbn)