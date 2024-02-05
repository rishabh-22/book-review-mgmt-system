from sqlalchemy import Column, Integer, String, ForeignKey, Float
from db_handler import Base


class Books(Base):
    """
    This is a model class which is having the book table structure with all the constraints
    """
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    title = Column(String(255), index=True, nullable=False)
    author = Column(String(255), index=True, nullable=False)
    author_email = Column(String(255), index=True, nullable=False)
    publication_year = Column(String(4), nullable=False)
    price = Column(Float, nullable=True)


class Reviews(Base):
    """
    This is a model class which is having the review table structure with all the constraints
    """
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    book_id = Column(Integer, ForeignKey("books"))
    text = Column(String(255), nullable=False)
    rating = Column(Float, nullable=False)
