import logging
from fastapi import APIRouter, Request
from app.schema.users import RequestUserSchema
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.api.utils import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, HTTPException, Depends
from  app.schema.users import RequestUserSchema


class CRUDUser:

    def create(self, db, *, user: RequestUserSchema) -> User:
        db_user = User(name=user.name, hashed_password=user.password, email=user.email, phone=user.phone,
                       is_active=True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

