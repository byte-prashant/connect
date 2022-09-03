import logging
from typing import List
from fastapi import APIRouter, Depends, status
from app.schema.request_type import RequirementTypeSchema, RequestTypeSchema
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.request_type import RequestType
from fastapi_versioning import version
from fastapi_versioning import versioned_api_route
from app.schema.request_type import ResposnseRequirementTypeSchema
requirement_router = APIRouter(prefix="/requirement")
requirement_router_v1_1 = APIRouter(prefix="/requirement", route_class=versioned_api_route(1, 1))



@requirement_router.post(
    "", tags=["Requirements"], status_code=status.HTTP_201_CREATED, response_model=ResposnseRequirementTypeSchema
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
        return {**req.dict(), "msg": "Created successfully"}

    else:
        return {**req.dict(), "msg": "This name already exist"}


@requirement_router.get(
    "", tags=["Requirements"], status_code=status.HTTP_200_OK, response_model= List[RequestTypeSchema]
)
async def get_requirement( db: Session = Depends(get_db)
):
    logging.info("Creating User")
    req = db.query(RequestType).filter(RequestType.is_active==True).all()
    print(req)
    for r in req:
        print(r.name)

    return req



@requirement_router_v1_1.get(
    "", tags=["Requirements"]
)
async def get_requirement( db: Session = Depends(get_db)
):
    logging.info("Getting user User")
    req = db.query(RequestType).filter(RequestType.is_active==True).all()
    print(req)
    return {**req.dict(), "msg": "This is version 1.1 api"}

