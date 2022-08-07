import logging
from fastapi import APIRouter, Depends
from schema.users import RequestUserSchema, ResponseUserSchema
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User


user_router = APIRouter(prefix="/users")


@user_router.post(
    "/createUser", tags=["users"]
)
async def create_user(
    user: RequestUserSchema, db: Session = Depends(get_db)
):
    logging.info("Creating User")
    existing_user = db.query(User).filter(User.phone == user.phone).first()
    if not existing_user:
        db_user = User(name=user.name, email=user.email, phone=user.phone, is_active=True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return user
    else:
        return {"msg": "User already exists with given phone no"}