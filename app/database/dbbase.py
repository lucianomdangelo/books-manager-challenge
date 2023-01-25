from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

Base = declarative_base()

DATABASE_URL = settings.DATABASE_URL.format(
    dbusername = settings.dbusername, 
    dbpassword = settings.dbpassword, 
    dbname = settings.dbname,
    dbcontainername = settings.dbcontainername, 
    dbport = settings.dbport
)
engine = create_engine(DATABASE_URL)

# DATABASE_URL = settings.DATABASE_URL
# engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
