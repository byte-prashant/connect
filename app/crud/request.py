from app.models.user import User
from app.api.utils import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, HTTPException, Depends
from  app.schema.request import RequestHelpSchema, CreateRequestSchema
from app.models.requests import Request


class CRUDRequest:

    def create(self, db, *, request:CreateRequestSchema):
        db_req = Request(reference_no=request.reference_no, req_type_id=request.request_type, user_id=request.user_id,
                         lat=request.lat, long=request.long, is_active=True)
        db.add(db_req)
        db.commit()
        db.refresh(db_req)
        return db_req


