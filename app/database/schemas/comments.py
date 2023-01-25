from pydantic import BaseModel
from datetime import datetime

class Comments(BaseModel):
    id: int
    comment: str
    books_id: int

    class Config:
        orm_mode = True