from fastapi import HTTPException

from app.database.crud.comments import comments_crud
from app.database.errors import NotFoundOnDBException, AlreadyExistsOnDBException

def get_comment_from_db(comment_id: str):
    comment_in_db = comments_crud.get_comment_by_id(comment_id)
    if not comment_in_db:
        raise HTTPException(status_code=404, detail="Comment id does not correspond to a comment on the system")
    return comment_in_db

def get_all_comments_of_book_from_db(isbn: str):
    all_comments_of_book_from_db = comments_crud.get_all_comments(isbn)
    if not all_comments_of_book_from_db:
        raise HTTPException(status_code=404, detail="No comments of this book were found on the system")
    return all_comments_of_book_from_db

def create_comment_of_book_in_db(isbn: str, comment: str):
    try:
        comment_created = comments_crud.create(isbn, comment)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=409, detail="The ISBN it's does not exists on the system")

    return comment_created

def update_comment_in_db(isbn: str, comment_id: str, comment: str):
    try: 
        comment_updated = comments_crud.update(isbn, comment_id, comment)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=409, detail="Comment not found")

    return comment_updated

def delete_comment_in_db(comment_id: str):
    try: 
        comment_deleted = comments_crud.delete(comment_id)
    except NotFoundOnDBException as error:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment_deleted