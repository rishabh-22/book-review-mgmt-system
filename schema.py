from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    author_email: str
    publication_year: int
    price: float = 0

    class Config:
        orm_mode = True


class BookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    publication_year: int
    price: float = 0


class Review(BaseModel):
    book_id: int
    text: str
    rating: float

    class Config:
        orm_mode = True
