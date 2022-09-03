from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.api.utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError
from app.schema.loginattempt import TokenPayload, SystemUser
from app.db.database import get_db
from app.models.user import User
from app.config import settings

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl= settings.TOKEN_URL,
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth), db: Session = Depends(get_db)) -> SystemUser:
    try:

        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print("=============================================", token_data.sub)
    user = db.query(User).filter_by(phone=token_data.sub).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return SystemUser(phone=user.phone, password=user.hashed_password, id=user.id)