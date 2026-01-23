from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel,ConfigDict # EmailStr, 

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: int
    total_copies: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available_copies: int

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass 

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

from enum import Enum

class LoanStatus(str, Enum):
    borrowed = "borrowed"
    returned = "returned"
    overdue = "overdue"

class LoanBase(BaseModel):
    book_id : int
    user_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: LoanStatus

class LoanCreate(BaseModel):
    book_id: int
    user_id: int

class Loan(LoanBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BookBorrowRequest(BaseModel):
    user_id: int

class BookReturnRequest(BaseModel):
    loan_id: int
