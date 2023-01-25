from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.dbbase import Base

class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True)
    info = Column(String)
    
    comments = relationship("Comments", cascade="all,delete")
    
