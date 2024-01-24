# build a schema using pydantic
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    rating: int
    author_id: int

    class Config:
        # orm_mode = True
        from_attributes = True

class FullBook(BaseModel):
    id:int
    title: str
    rating: int
    author_id: int

    class Config:
        # orm_mode = True
        from_attributes = True

class Author(BaseModel):
    name:str
    surname:str
    age:int

    class Config:
        # orm_mode = True
        from_attributes = True
        
