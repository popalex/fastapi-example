from pydantic import BaseModel

# Schema for input when creating an author (no ID)
class AuthorCreate(BaseModel):
    name: str
    surname: str
    age: int

    class Config:
        # orm_mode = True
        from_attributes = True

# Schema for output after creating an author (with ID)
class AuthorResponse(BaseModel):
    id: int  # ID will be included in the response
    name: str
    surname: str
    age: int

    class Config:
        # orm_mode = True
        from_attributes = True

# No changes needed for books if they're fine as-is
class Book(BaseModel):
    title: str
    rating: float
    author_id: int

    class Config:
        # orm_mode = True
        from_attributes = True

class FullBook(BaseModel):
    id: int
    title: str
    rating: float
    author_id: int

    class Config:
        # orm_mode = True
        from_attributes = True
