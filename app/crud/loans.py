from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Loan

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
