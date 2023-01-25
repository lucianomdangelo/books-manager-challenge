from pydantic import BaseModel
from app.schemas.comments import Comments

class Books(BaseModel):
    id: int
    isbn: str
    info: str
    comments: list[Comments] = []
    
    class Config:
        orm_mode = True