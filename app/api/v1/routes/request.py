import logging
from fastapi import APIRouter, Depends, status
from typing import List
from app.schema.request import RequestHelpSchema,CreateRequestSchema, CreateMultipleRequest, ResponseHelpSchema, SeekHelpSchema
from app.schema.loginattempt import SystemUser
from app.schema.users import RequestUserSchema
from app.schema.assistance import CreateAssistanceSchema, AssistanceSchema, RequestAssistanceSchema
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.models.requests import Request
from app.models.request_type import RequestType
from app.models.assistance import Assistance
from app.models.user import User
import uuid
from app.worker.celery_app import sms_worker
from app.api.deps import get_current_user
from app.crud.request import CRUDRequest
from app.crud.users import CRUDUser
from app.crud.assistance import CRUDAssistance
from app.db.database import get_db_conn
##  reference no's can be pre-populated in redis and used

help_router = APIRouter(prefix="/needs")

DEFAULT_USER_PHONE = "9560109169"
DEFAULT_USER_NAME = "GOD"
DEFAULT_PASSWORD = "GET_GOD"


@help_router.post(
    "", tags=["Needs"], response_model=ResponseHelpSchema
)
async def create_requirement(
    req: RequestHelpSchema, user: SystemUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    reference_no = str(uuid.uuid4())
    logging.info("God has been called")
    phone = DEFAULT_USER_PHONE
    if user.phone:
        phone = req.phone
    logging.debug("God has been called", phone)
    existing_req = db.query(User).filter(User.phone == phone)
    if not db.query(existing_req.exists()):
        logging.debug("Creating account for God")
        user = RequestUserSchema(name=DEFAULT_USER_NAME, phone=DEFAULT_USER_NAME, email="", password=DEFAULT_PASSWORD)
        db_user =  CRUDUser.create(db, user)
    existing_req = db.query(User).filter(User.phone == phone).first()

    existing_req_type = db.query(RequestType).get(req.request_type)
    db_req = CreateRequestSchema(reference_no=reference_no, request_type=existing_req_type.id, user_id=existing_req.id, lat=req.lat, long=req.long)
    db_req_obj = CRUDRequest().create(db=db, request=db_req)
    task = sms_worker.delay("Your request registered successfully. Ref no is {}".format(reference_no), "+919560109169")
    print(task.get())
    return { **req.dict(), "msg": "Request registered", "reference_no": reference_no}


@help_router.get("", tags=["Needs"], status_code=status.HTTP_200_OK, response_model=List[SeekHelpSchema])
def get_seeker_in_radius(lat:str,long:str,dist:float,db: Session = Depends(get_db)):
    """

    :param req:

                {
                  "lat": "28.656653326685582",
                  "long": "77.28727608919144",
                  "distance":10

                }
    :param db:
    :return:
    """
    latitude = lat
    longitude = long
    dis = dist
    result = []
    sql_query = f"SELECT id,lat,long,req_type_id,distance FROM ( SELECT *,( ( ( acos( sin(({ latitude } * pi() / 180)) * sin((CAST(lat AS float) * pi() / 180)) + cos(({latitude} * pi() / 180)) * cos(( CAST(lat AS float) * pi() / 180)) * cos( ( ({ longitude } - CAST(long AS float)) * pi() / 180 ) ) ) ) * 180 / pi() ) * 60 * 1.1515 * 1.609344 ) as distance FROM request ) request WHERE distance <= { dis } LIMIT 15;"
    with get_db_conn() as conn:
        cur_result = conn.exec_driver_sql(sql_query, {})
        for row in cur_result:
            result.append(row)
    return result


@help_router.post("/create_requests/", tags=["Needs"], status_code=status.HTTP_201_CREATED)
def register_bulk_help(req: CreateMultipleRequest,
                          db: Session = Depends(get_db)):
    """

    :param req:

            {
                  "seeker": [
                        {
                          "lat": "28.6566650950006",
                          "long": "77.29726804256438"
                        },

                       {
                          "lat": "28.6566650950006",
                          "long": "77.39726804256438"
                        },



                  ]
            }
    :param db:
    :return:
    """
    seekers = req.seeker

    existing_req = db.query(User).filter(User.phone == DEFAULT_USER_PHONE).first()
    if not existing_req:
        return {"msg": "The god has not registered himself yet, so you have to enter his Data"}

    for seeker in list(seekers):
        reference_no = str(uuid.uuid4())
        existing_req_type = db.query(RequestType).get(seeker['request_type_id'])
        req_obj = CreateRequestSchema(reference_no=reference_no, request_type=existing_req_type.id, user_id=existing_req.id,
                                   lat=seeker['lat'], long=seeker['long'])
        db_req_obj = CRUDRequest().create(db=db, request=req_obj)

    return {"msg": "Entries successfully registered"}


@help_router.post(
    "/{need_id}/assistance", tags=["Needs"], status_code=status.HTTP_200_OK
)
async def create_assistance(
    req: CreateAssistanceSchema, user:SystemUser = Depends(get_current_user), db: Session = Depends(get_db),need_id=int
):
    """
       - This only includes feature when  user who gives assistance is loggedin

    """
    user_id = user.id
    assistance = AssistanceSchema(request_id=need_id, user_id=user_id, lat=req.lat, long=req.long )
    obj = CRUDAssistance().create(db=db, assis=assistance)
    return {"msg":"Success! Assistance Registered."}


@help_router.put(
    "/{need_id}/assistance/{assist_id}", tags=["Needs"], status_code=status.HTTP_200_OK
)
async def approve_assistance( user:SystemUser = Depends(get_current_user), db: Session = Depends(get_db),need_id=int, assist_id=int
):
    """
       - This api is used to approve the assistance provided by user

    """
    user_id = user.id
    #assistance = AssistanceSchema(request_id=need_id, user_id=user_id, lat=req.lat, long=req.long )
    obj = CRUDAssistance().update(db=db, assist_id=assist_id)
    return {"msg":"Success! Assistance Approved."}





