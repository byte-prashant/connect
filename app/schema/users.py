
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    hashed_password: str
    is_active: bool

    class Config:
        orm_mode = True


class RequestUserSchema(BaseModel):
    email: str
    name: str
    phone: str
    password: str

    class Config:
        orm_mode = True

class RequestOtpUserSchema(BaseModel):
    email: str
    name: str
    phone: str
    otp: str

    class Config:
        orm_mode = True


class ResponseUserSchema(BaseModel):
    name: str
    phone: str
    msg : str
    access_token: Optional[str] = None
    class Config:
        orm_mode = True

