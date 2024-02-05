from typing import List

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

import mailer
import utils
import model
import schema
from db_handler import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/books/all', response_model=List[schema.BookResponse])
def get_all_books(author: str = None, publication_year: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = utils.get_books(db=db, skip=skip, limit=limit, author=author, publication_year=publication_year)
    return books


@app.get('/books/{book_id}}', response_model=schema.BookResponse)
def get_book_via_book_id(book_id: int,  db: Session = Depends(get_db)):
    book = utils.get_book_via_book_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found with this ID")
    return book


@app.post('/books/add')
def add_new_book(book: schema.Book, db: Session = Depends(get_db)):
    if utils.add_book(db=db, book=book):
        return {"message": "success"}
    raise HTTPException(status_code=500, detail="There was an error adding the book.")


@app.post('/review/add')
def add_new_review(review: schema.Review, tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if not utils.validate_book_id(db=db, book_id=review.book_id):
        raise HTTPException(status_code=400, detail="Book ID is invalid.")
    if utils.add_review(db=db, review=review):
        mail_data = utils.get_review_email_data(db=db, book_id=review.book_id, review_text=review.text)
        tasks.add_task(mailer.send_mail, mail_data)
        return {"message": "success"}
    raise HTTPException(status_code=500, detail="There was an error adding the review.")


@app.get('/books/{book_id}/review/all', response_model=List[schema.Review])
def get_all_reviews(book_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = utils.get_all_reviews_for_book(db=db, book_id=book_id, skip=skip, limit=limit)
    return reviews


@app.get('/books/{book_id}/rating')
def get_book_rating(book_id: int, db: Session = Depends(get_db)):
    rating = utils.get_rating_for_book(db=db, book_id=book_id)
    return rating
