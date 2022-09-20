import logging
import random
from fastapi import APIRouter, Request
from app.schema.users import RequestUserSchema, ResponseUserSchema, RequestOtpUserSchema
from app.schema.loginattempt import LoginAttemptSchema, OTPSchema
from app.crud.users import CRUDUser
from app.crud.loginattempt import CRUDLoginAttempt
from app.db.database import get_db
from app.api.auth_managers import OtpLoginManager
from app.models.user import User
from app.models.loginattempt import LoginAttempt
from app.utils import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, HTTPException, Depends
from app.worker.celery_app import sms_worker
from sqlalchemy.orm import Session

# ------------------------------------------------
# create user using  phone no as username and password
# create user using phone_no as username and otp as password
# ------------------------------------------------

jwt_router = APIRouter(prefix="/profile")
DEFAULT_USER_PASS = "CONNECT"

@jwt_router.post(
    "/signup", tags=["Profile"], response_model= ResponseUserSchema
)
async def create_user(request:Request,
    user: RequestUserSchema, db: Session = Depends(get_db)
):
    logging.info("Creating User")
    existing_user = db.query(User).filter(User.phone == user.phone, User.is_active == True).first()
    if not existing_user:
        obj = CRUDUser().create(db, user=user)
        return {"phone": obj.phone, "name": obj.name, "msg": "User Registered Successfully"}
    else:
        return {"phone": user.phone, "name": user.name, "msg": "User already exists with given phone no"}


@jwt_router.post('/login', tags=["Profile"], summary="Create access token")
async def login( request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == form_data.username, User.is_active == True).first()
    if not user :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect phone or password"
        )

    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect phone or password"
        )

    return {
        "access_token": create_access_token(user.phone)
    }


@jwt_router.post("/otp", tags=['Profile'], summary=["Get an otp to login/signup"])
async def get_otp(req: OTPSchema, db: Session = Depends(get_db)):

    otp = random.randint(1000, 9999)
    print("your otp is", otp)
    existing_user = db.query(LoginAttempt).filter(LoginAttempt.identifier == req.phone).first()
    if existing_user:
        login_schema = LoginAttemptSchema(identifier=req.phone, otp=otp)
        obj = CRUDLoginAttempt().update(db=db, login=login_schema)
    else:
        login_schema = LoginAttemptSchema(identifier=req.phone, otp=otp)
        obj = CRUDLoginAttempt().create(db=db, login=login_schema)
    msg= "Otp to login is {}".format(otp)
    task = sms_worker.delay(msg, req.phone)
    print(task.get())
    return {
            "msg": "Otp sent"
    }


@jwt_router.post(
    "/otpLogin", tags=["Profile"], status_code=status.HTTP_200_OK, response_model= ResponseUserSchema
)
async def create_user(
    user: RequestOtpUserSchema, db: Session = Depends(get_db)
):
    logging.info("Creating User")
    if OtpLoginManager().verify_otp(session=db, identifier=user.phone, code=user.otp):

        existing_user = db.query(User).filter(User.phone == user.phone, User.is_active == True).first()
        if not existing_user:

            obj = CRUDUser().create(db, user=RequestUserSchema(name=user.name, phone=user.phone, email=user.email,password=DEFAULT_USER_PASS))
            return {"phone": obj.phone, "name": obj.name, "access_token": create_access_token(user.phone), "msg": "User Registered Successfully"}
        else:
            return {"phone": user.phone, "name": user.name,"access_token": create_access_token(user.phone), "msg": "User already exists with given phone no"}

    else:
        return {"phone": user.phone,"name": user.name, "msg": "Entered wrong otp"}






