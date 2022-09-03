from uuid import UUID
from typing import Any
from pydantic import BaseModel
from typing import Optional


class CommonError(Exception):
    code: str
    message: str
    additional: Any = None
    status: int = 400

    def content(self):
        return {
            "code": self.code,
            "message": self.message,
            "additional_info": self.additional,
        }


class UserOut(BaseModel):
    id: UUID
    phone: str


class SystemUser(BaseModel):
    password: str
    phone: str
    id: int


class ValidationError(CommonError):
    code = "validation_error"
    status = 422
    message = "The data submitted is not valid"

    def __init__(self, errors: dict):
        self.errors = errors

    @property
    def additional(self):
        return self.errors


class InvalidUserCredentials(CommonError):
    code = "invalid_user_credentials"
    message = "No user can be found matching provided credentials"
    status = 401


class InvalidOTP(CommonError):
    code = "invalid_otp"
    message = "The OTP provided is not valid"
    status = 401


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class LoginAttemptSchema(BaseModel):
    identifier: str
    otp: str


class UpdateLoginAttemptSchema(BaseModel):
    msg: Optional[str] = None
    otp: str
    identifier: str


class OTPSchema(BaseModel):
    phone: str