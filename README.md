# Book-Review management system

This repository holds the code for a book review management system made using FastAPI.
Below-mentioned are the features of the application:

## Features
### 1. Add and retrieve book(s)

- Add book
- Get book via book id
- Get all books

### 2. Add and retrieve reviews

- Add review and rating for a book
- Fetch rating for a book
- Fetch all reviews of a book

## APIs

#### Books

- fetch all books: `/books/all`
- fetch book via book id: `/books/{book_id}`
- Add new book: `/books/add`


#### Review

- Add review: `/review/add`
- fetch all reviews for a book: `/books/{book_id}/review/all`
- fetch rating of a book: `/books/{book_id}/rating`


# How to run the application

## Method 1:
- via make: `make`

## Method 2:
- via docker: `make container`

## Method 3:
- via command line: `uvicorn main:app --port 8000`