from pydantic import BaseModel,ConfigDict
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    content: str 

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str]
    year_published: Optional[int]
    summary: Optional[str]

    # class Config:
    #     orm_mode = True

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
