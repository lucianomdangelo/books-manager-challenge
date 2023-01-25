import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

from fastapi import FastAPI
from app.database.crud.books import books_crud
from app.database.crud.comments import comments_crud

from app.router.main_router import router
from app.database.dbbase import Base

from app.dependencies import get_db
from app.dependencies import db_session

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

app = FastAPI()
app.include_router(router)



@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)
    app.dependency_overrides[get_db] = lambda: db

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    db_session.set(db)
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def get_book(db):
    db_session.set(db)
    books_crud.create("9780140328721", "info")

@pytest.fixture
def get_book_and_comment(db):
    db_session.set(db)
    books_crud.create("9780140328721", "info")
    comments_crud.create("9780140328721", "comment")