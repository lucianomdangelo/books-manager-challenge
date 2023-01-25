from app.database.dbbase import SessionLocal
from contextvars import ContextVar
from sqlalchemy.orm import Session

import requests

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_session: ContextVar[Session] = ContextVar('db_session')