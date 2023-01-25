from app.config import settings
from fastapi import HTTPException
import requests

def validate_isbn(isbn):
    return ((len(isbn) == 10 or len(isbn) == 13) and isbn.isdigit())
        

def provide_book_by_isbn(isbn: str):
    if not validate_isbn(isbn):
        raise HTTPException(status_code=400, detail="Please check the ISBN. It's must be 10 or 13 digits length")
    info = requests.get(settings.BOOKS_PROVIDER_URL.format(isbn = isbn))

    if info.text == '{}':
        raise HTTPException(status_code=404, detail="Book not found on the books provider")
    
    return info.json()
