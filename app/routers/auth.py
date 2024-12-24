from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.repository import auth_repository

router = APIRouter(prefix="/api/auth", tags=["Login"])

@router.post('/login', status_code=status.HTTP_200_OK)
def get_login(login: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    jwt_token = auth_repository.auth_user(db, login)
    return jwt_token
