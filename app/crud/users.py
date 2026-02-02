from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.db.models import User

# User CRUD

def create_user(db: Session, user: schemas.UserCreate) -> User:
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.execute(select(User).offset(skip).limit(limit)).scalars().all()
