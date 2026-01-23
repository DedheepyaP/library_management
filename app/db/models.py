from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from app.db.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    publication_year = Column(Integer, nullable=False)
    genre = Column(String, nullable=True)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)

    
    loans = relationship(
        "Loan",
        back_populates="book",
        cascade="all, delete-orphan"
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # One-to-many: User → Loans
    loans = relationship(
        "Loan",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class LoanStatus(str, Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    borrow_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    due_date = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(days=14)
    )

    return_date = Column(DateTime, nullable=True)

    status = Column(
        String,
        nullable=False,
        default=LoanStatus.BORROWED.value
    )

    # Many-to-one relationships
    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")
