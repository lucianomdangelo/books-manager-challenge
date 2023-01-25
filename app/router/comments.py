from fastapi import APIRouter, HTTPException, Request, Depends
from app.services import comments as comments_service

from sqlalchemy.orm import Session
from contextvars import ContextVar
from app.dependencies import get_db, db_session


router = APIRouter(prefix="/books/{isbn}/comments", tags=["/books/{isbn}/comments"])



@router.get("/")
def get_all_comments_of_book_from_db(isbn: str, db: Session = Depends(get_db)):
    db_session.set(db)
    return comments_service.get_all_comments_of_book_from_db(isbn)

@router.get("/{comment_id}")
def get_comment_of_book_from_db(comment_id: str, db: Session = Depends(get_db)):
    if not comment_id.isdigit():
        raise HTTPException(status_code=422, detail="the comment id must be a digit")

    db_session.set(db)
    return comments_service.get_comment_from_db(comment_id)

@router.post("/")
async def create_comment_db(isbn: str, request: Request, db: Session = Depends(get_db)):
    db_session.set(db)
    try:
        request_json = await request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameter 'comment' on request body or its imcomplete")

    if not (request_json and 'comment' in request_json and request_json['comment']):
        raise HTTPException(status_code=422, detail="Missing parameter 'comment' on request body or its imcomplete")

    comment = request_json['comment']

    return comments_service.create_comment_of_book_in_db(isbn, comment)

@router.put("/{comment_id}")
async def update_comment_db(isbn: str, comment_id: str, request: Request, db: Session = Depends(get_db)):
    if not comment_id.isdigit():
        raise HTTPException(status_code=422, detail="the comment id must be a digit")

    try:
        request_json = await request.json()
    except:
        raise HTTPException(status_code=422, detail="Missing parameter 'comment' on request body or its imcomplete")

    if not (request_json and 'comment' in request_json and request_json['comment']):
        raise HTTPException(status_code=422, detail="Missing parameter 'comment' on request body or its imcomplete")
    comment = request_json['comment']
    
    db_session.set(db)
    return comments_service.update_comment_in_db(isbn, comment_id, comment)

@router.delete("/{comment_id}")
def delete_comment_db(isbn: str, comment_id: str, db: Session = Depends(get_db)):
    if not comment_id.isdigit():
        raise HTTPException(status_code=422, detail="the comment id must be a digit")
    db_session.set(db)
    return comments_service.delete_comment_in_db(comment_id=comment_id)