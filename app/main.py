from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.db.database import get_db

app = FastAPI(title="Libro Library API")


# Book Endpoints

@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, book)
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip, limit)


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)



@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    crud.delete_book(db, book_id)
    return {"detail": "Book deleted successfully"}


@app.post("/books/{book_id}/borrow", response_model=schemas.Loan)
def borrow_book(
    book_id: int,
    request: schemas.BookBorrowRequest,
    db: Session = Depends(get_db)
):
    return crud.borrow_book(db, book_id, request.user_id)


# User Endpoints

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)


# Loan Endpoints

@app.get("/loans/", response_model=list[schemas.Loan])
def read_loans(
    user_id: int | None = None,
    book_id: int | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_loans(db, user_id, book_id, status, skip, limit)


@app.get("/loans/{loan_id}", response_model=schemas.Loan)
def read_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = crud.get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@app.post("/loans/{loan_id}/return", response_model=schemas.Loan)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    return crud.return_book(db, loan_id)
