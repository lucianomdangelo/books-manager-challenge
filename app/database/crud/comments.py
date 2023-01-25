from sqlalchemy.orm import Session
from app.dependencies import db_session
from app.database.models.comments import Comments as CommentsModel
from app.database.models.books import Books as BooksModel
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException
from app.config import settings

class CommentsCRUD():
    def get_all_comments(self, isbn: str):
        db = db_session.get()
        return db.query(CommentsModel).join(BooksModel).filter(BooksModel.isbn == isbn ).offset(0).limit(settings.DB_LIST_LIMIT).all()

    def get_comment_by_id(self, comment_id):
        db = db_session.get()
        return db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()

    def create(self, isbn: str, comment: str):
        db = db_session.get()
        ## Search book
        book_in_db = db.query(BooksModel).filter(BooksModel.isbn == isbn).first()
        if not book_in_db:
            raise NotFoundOnDBException
        ## Create Comment
        db_comment = CommentsModel()
        db_comment.books_id = book_in_db.id
        db_comment.comment = comment

        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def update(self, isbn: str, comment_id: str, comment: str):
        db = db_session.get()
        db_comment = self.get_comment_by_id(comment_id)
        if not db_comment:
            raise NotFoundOnDBException

        db_comment.comment = comment
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    def delete(self, comment_id: str):
        db = db_session.get()
        db_comment = db.query(CommentsModel).get(comment_id)

        if not db_comment:
            raise NotFoundOnDBException

        db.delete(db_comment)
        db.commit()
        return db_comment

comments_crud = CommentsCRUD()