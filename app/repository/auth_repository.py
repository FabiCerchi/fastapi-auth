from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash
from sqlalchemy.orm import Session
from app.token import Token

def auth_user(db: Session, login):
    user = db.query(models.User).filter(models.User.username == login.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credentials"
        )

    if not Hash.verify_password(login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid credentials",
        )

    try:
        access_token = Token.create_access_token(
            data={"sub": user.username}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the access token {e}"
        )

    return {'access_token':access_token, 'token_type':"bearer"}
