from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.db.models import Book, User, Loan, LoanStatus

# Book

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
        raise HTTPException(status_code=404, detail="Book not found")

    # Keep available copies consistent if total changes
    if book_update.total_copies < (book.total_copies - book.available_copies):
        raise HTTPException(
            status_code=400,
            detail="Cannot reduce total copies below number of currently borrowed copies"
        )

    borrowed_count = book.total_copies - book.available_copies
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
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()

    # User
def create_user(db: Session, user: schemas.UserCreate) -> User:
    new_user = User(
        name=user.name,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.execute(select(User).offset(skip).limit(limit)).scalars().all()

#loan

def get_loan(db: Session, loan_id: int) -> Optional[Loan]:
    return db.get(Loan, loan_id)

def get_loans(
    db: Session,
    user_id: int = None,
    book_id: int = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100
) -> List[Loan]:
    query = select(Loan)

    if user_id is not None:
        query = query.where(Loan.user_id == user_id)
    if book_id is not None:
        query = query.where(Loan.book_id == book_id)
    if status is not None:
        query = query.where(Loan.status == status)

    return db.execute(query.offset(skip).limit(limit)).scalars().all()

#borrow

def borrow_book(db: Session, book_id: int, user_id: int) -> Loan:
    with db.begin():  # transaction start
        book = db.execute(
            select(Book).where(Book.id == book_id).with_for_update()
        ).scalar_one_or_none()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if book.available_copies <= 0:
            raise HTTPException(status_code=400, detail="No copies available")

        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        book.available_copies -= 1

        new_loan = Loan(
            book_id=book_id,
            user_id=user_id,
            borrow_date=datetime.now(timezone.utc),
            due_date=datetime.now(timezone.utc) + timedelta(days=14),
            status=LoanStatus.BORROWED
        )

        db.add(book)
        db.add(new_loan)

    return new_loan

def return_book(db: Session, loan_id: int) -> Loan:
    with db.begin():
        loan = db.execute(
            select(Loan).where(Loan.id == loan_id).with_for_update()
        ).scalar_one_or_none()

        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        if loan.status != LoanStatus.BORROWED:
            raise HTTPException(status_code=400, detail="Loan is not active")

        book = db.execute(
            select(Book).where(Book.id == loan.book_id).with_for_update()
        ).scalar_one()

        book.available_copies += 1
        loan.status = LoanStatus.RETURNED
        loan.return_date = datetime.now(timezone.utc)

        db.add(book)
        db.add(loan)

    return loan
