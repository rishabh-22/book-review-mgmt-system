from sqlalchemy import func
from sqlalchemy.orm import Session
import model
import schema


def get_book_count(db: Session):
    """
    This method will return all books which are present in database
    :param db: session object
    :return: count of all the books from database
    """
    return db.query(model.Books).count()


def get_review_count(db: Session, book_id):
    """
    This method will return all books which are present in database
    :param db: session object
    :param book_id:
    :return: count of all the reviews from database
    """
    return db.query(model.Reviews).filter(model.Reviews.book_id == book_id).count()


def get_book_ids(db: Session):
    """
    This method returns all the available book ids
    :param db:
    :return: a list of all book ids
    """
    books = get_books(db)
    return [book.book_id for book in books]


def get_books(db: Session, author=None, publication_year=None, skip: int = 0, limit: int = 100):
    """
    This method will return all books which are present in database
    :param db:
    :param author:
    :param publication_year:
    :param skip: the number of rows to skip before including them in the result
    :param limit: to specify the maximum number of results to be returned
    :return: all the rows from database
    """

    if author and publication_year:
        return (db.query(model.Books).
                filter(model.Books.author == author, model.Books.publication_year == publication_year).
                offset(skip).limit(limit).all())
    if publication_year:
        return (db.query(model.Books).filter(model.Books.publication_year == publication_year).
                offset(skip).limit(limit).all())
    if author:
        return (db.query(model.Books).filter(model.Books.author == author).
                offset(skip).limit(limit).all())
    return db.query(model.Books).offset(skip).limit(limit).all()


def get_book_via_book_id(db: Session, book_id):
    return db.query(model.Books).filter(model.Books.book_id == book_id).first()


def add_book(db: Session, book: schema.Book):
    """
    this method will add a new record to database, and perform the commit and refresh operation to db
    :param db:
    :param book:
    :return: a dictionary object of the record which has inserted
    """
    try:
        book = model.Books(
            title=book.title,
            author=book.author,
            author_email=book.author_email,
            publication_year=book.publication_year,
            price=book.price
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return True
    except Exception as e:
        print("Error while adding book", e)
        return False


def add_review(db: Session, review: schema.Review):
    """
    this method will add a new record to database, and perform the commit and refresh operation to db
    :param db:
    :param review:
    :return: a dictionary object of the record which has inserted
    """
    try:
        book_ids = get_book_ids(db)
        if review.book_id not in book_ids:
            raise Exception("book id does not exist")
        review = model.Reviews(
            book_id=review.book_id,
            text=review.text,
            rating=review.rating,
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        return True
    except Exception as e:
        print("Error while adding review", e)
        return False


def get_all_reviews_for_book(db: Session, book_id, skip: int = 0, limit: int = 100):
    """
    this method will return all the reviews for a given book
    :param db:
    :param book_id:
    :param skip:
    :param limit:
    :return: list of all the reviews related to book_id
    """
    return db.query(model.Reviews).filter(model.Reviews.book_id == book_id).offset(skip).limit(limit).all()


def get_rating_for_book(db: Session, book_id):
    rating = db.query(func.sum(model.Reviews.rating).label("sum_rating")).filter(model.Reviews.book_id ==
                                                                                 book_id).first()[0]
    total_count = get_review_count(db, book_id)
    return rating / total_count


def validate_book_id(db: Session, book_id: int):
    book_ids = get_book_ids(db)
    if book_id not in book_ids:
        return False
    return True


def get_review_email_data(db: Session, book_id, review_text):
    return {
        'to': [db.query(model.Books).filter(model.Books.book_id == book_id).first().author_email],
        'subject': "New Review for your book",
        'body': review_text
    }
