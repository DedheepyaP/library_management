from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.db.models import Book

# Book CRUD

def create_book(db: Session, book: schemas.BookCreate) -> Book:
    new_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        publication_year=book.publication_year,
        total_copies=book.total_copies,
        available_copies=book.total_copies
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.get(Book, book_id)


def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
    return db.execute(select(Book).offset(skip).limit(limit)).scalars().all()


def update_book(db: Session, book_id: int, book_update: schemas.BookCreate) -> Book:
    book = db.get(Book, book_id)
    if not book:
        raise ValueError("Book not found")

    borrowed_count = book.total_copies - book.available_copies
    if book_update.total_copies < borrowed_count:
        raise ValueError(
        "Cannot reduce total copies below currently borrowed copies"
        )

    book.title = book_update.title
    book.author = book_update.author
    book.isbn = book_update.isbn
    book.publication_year = book_update.publication_year
    book.total_copies = book_update.total_copies
    book.available_copies = book_update.total_copies - borrowed_count

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> None:
    book = db.get(Book, book_id)
    if not book:
        raise ValueError("Book not found")
    db.delete(book)
    db.commit()
