import logging
from fastapi import APIRouter, Depends
from schema.request_type import RequirementTypeSchema, ResposnseRequirementTypeSchema
from sqlalchemy.orm import Session
from db.database import get_db
from models.request_type import RequestType


requirement_router = APIRouter(prefix="/requirement")



@requirement_router.post(
    "/createRequirement", tags=["Create requirement"], response_model=ResposnseRequirementTypeSchema
)
async def create_requirement(
    req: RequirementTypeSchema, db: Session = Depends(get_db)
):
    logging.info("Creating Reuest Type")
    existing_req = db.query(RequestType).filter(RequestType.name == req.name.upper()).first()
    #print(db.query(existing_req.exists()))
    if not existing_req:
        db_req = RequestType(name=req.name.upper(),  is_active=True)
        logging.info("Creating Reuest no exist Type")
        db.add(db_req)
        db.commit()
        db.refresh(db_req)
        return req
    else:
        return {**req.dict(), "msg": "This name already exist"}

@requirement_router.get(
    "/", tags=["get requirements "]
)
async def get_requirement( db: Session = Depends(get_db)
):
    logging.info("Creating User")
    req = db.query(RequestType).filter(RequestType.is_active==True).all()
    print(req)
    return req
