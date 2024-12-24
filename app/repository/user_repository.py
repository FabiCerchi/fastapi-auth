from sqlalchemy.orm import Session
from app.schemas import UpdateUser
from app.db import models
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.hashing import Hash
from typing import List, Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user) -> models.User:
    name = user.name
    last_name = user.last_name
    age = user.age
    email = user.email
    username = user.username
    password = user.password
    address = user.address
    try:
        new_user = models.User(name=name,
                               last_name=last_name,
                               age=age, email=email,
                               username=username,
                               password=Hash.get_password_hash(password),
                               address=address)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail=str(e))

    return new_user


def get_user(db: Session) -> Optional[List[models.User]]:
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    user = db.query(models.User).filter(models.User.id == user_id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user.first()


def update_user(db: Session, user_id: int, user: UpdateUser):
    user_to_update = db.query(models.User).filter(models.User.id == user_id)

    if not user_to_update.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    try:
        user_to_update.update(user.model_dump(exclude_unset=True))
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    return {"res": "Usuario actualizado"}


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user.delete(synchronize_session=False)
    db.commit()

    return {"res": "Usuario eliminado"}
