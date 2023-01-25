from sqlalchemy.orm import Session
from app.dependencies import db_session
from app.database.models.books import Books as  BooksModel
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException
from app.config import settings

class BooksCRUD():
    def get_by_isbn(self, isbn: str):
        db = db_session.get()
        return db.query(BooksModel).filter(BooksModel.isbn == isbn).first()

    def get_all_books(self):
        db = db_session.get()
        return db.query(BooksModel).offset(0).limit(settings.DB_LIST_LIMIT).all()

    def create(self, isbn: str, info: str):
        db = db_session.get()
        book_in_db = books_crud.get_by_isbn(isbn)
        if book_in_db:
            raise AlreadyExistsOnDBException

        db_book = BooksModel(isbn = isbn, info = info)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    def update(self, isbn: str, info: str):
        db = db_session.get()
        db_book = self.get_by_isbn(isbn)
        if not db_book:
            raise NotFoundOnDBException
       
        db_book.info = info
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    def delete(self, isbn: str):
        db = db_session.get()
        db_book = self.get_by_isbn(isbn)
        if not db_book:
            raise NotFoundOnDBException
        db.delete(db_book)
        db.commit()
        return db_book

books_crud = BooksCRUD()