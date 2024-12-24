from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import User, ShowUser, UpdateUser, TokenData
from app.db.db import get_db
from app.repository import user_repository
from app.oauth import OAuth


router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = user_repository.create_user(db, user)
    return new_user

@router.get("/", response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db), current_user: TokenData = Depends(OAuth.get_current_user)):
    users = user_repository.get_user(db)
    return users


@router.get("/{user_id}", response_model=ShowUser, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(OAuth.get_current_user)):
    user = user_repository.get_user_by_id(db, user_id)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(OAuth.get_current_user)):
    res = user_repository.delete_user(db, user_id)
    return res


@router.patch("/{user_id}", status_code= status.HTTP_200_OK)
def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db) , current_user: TokenData = Depends(OAuth.get_current_user)):
    res = user_repository.update_user(db, user_id, user)
    return res