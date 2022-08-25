import logging
from fastapi import APIRouter, Depends
from schema.request import RequestHelpSchema, ResponseHelpSchema
from sqlalchemy.orm import Session
from db.database import get_db
from models.requests import Request
from models.request_type import RequestType
from models.user import User
import uuid
from worker.celery_app import sms_worker

##  reference no's can be pre-populated in redis and used

help_router = APIRouter(prefix="/fildHelp")

DEFAULT_USER_PHONE = "9560109169"
DEFAULT_USER_NAME = "GOD"

@help_router.post(
    "/fildHelp", tags=["Ask for Help"], response_model=ResponseHelpSchema
)
async def create_requirement(
    req: RequestHelpSchema, db: Session = Depends(get_db)
):
    reference_no = str(uuid.uuid4())
    logging.info("God has been called")
    phone = DEFAULT_USER_PHONE
    if req.phone:
        phone = req.phone
    logging.debug("God has been called", phone)
    existing_req = db.query(User).filter(User.phone == phone)
    if not db.query(existing_req.exists()):
        logging.debug("Creating account for God")
        db_user = User(name=DEFAULT_USER_NAME, phone=DEFAULT_USER_NAME, is_active=True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    existing_req = db.query(User).filter(User.phone == phone).first()

    existing_req_type = db.query(RequestType).get(req.request_type)
    db_req = Request(reference_no=reference_no, req_type_id=existing_req_type.id, user_id=existing_req, lat=req.lat, long=req.long,  is_active=True)
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    task = sms_worker.delay("Your request registered successfully. Ref no is {}".format(reference_no), "+919560109169")
    print(task.get())
    return { **req.dict(), "msg":"Request registered", "reference_no":reference_no}

"""
SELECT * FROM (
    SELECT *, 
        (
            (
                (
                    acos(
                        sin(( $LATITUDE * pi() / 180))
                        *
                        sin(( `latitud_fieldname` * pi() / 180)) + cos(( $LATITUDE * pi() /180 ))
                        *
                        cos(( `latitud_fieldname` * pi() / 180)) * cos((( $LONGITUDE - `longitude_fieldname`) * pi()/180)))
                ) * 180/pi()
            ) * 60 * 1.1515 * 1.609344
        )
    as distance FROM `myTable`
) myTable
WHERE distance <= $DISTANCE_KILOMETERS
LIMIT 15;
"""
