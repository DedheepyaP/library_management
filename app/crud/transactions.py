from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Book, User, Loan, LoanStatus

def borrow_book(db: Session, book_id: int, user_id: int) -> Loan:
    with db.begin():
        book = db.execute(select(Book).where(Book.id==book_id).with_for_update()).scalar_one_or_none()
        if not book:
            raise ValueError("Book not found")
        if book.available_copies <= 0:
            raise ValueError("No available copies")
        user = db.get(User, user_id)
        if not user:
            raise ValueError("User not found")
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
        loan = db.execute(select(Loan).where(Loan.id==loan_id).with_for_update()).scalar_one_or_none()
        if not loan:
            raise ValueError("Loan not found")
        if loan.status != LoanStatus.BORROWED:
            raise ValueError("Loan is not active")
        book = db.execute(select(Book).where(Book.id==loan.book_id).with_for_update()).scalar_one()
        book.available_copies += 1
        loan.status = LoanStatus.RETURNED
        loan.return_date = datetime.now(timezone.utc)
        db.add(book)
        db.add(loan)
    return loan
