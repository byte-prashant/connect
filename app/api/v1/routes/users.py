from typing import List
from fastapi import status,APIRouter,FastAPI,Depends
from app.models.assistance import Assistance
from app.models.requests import Request
from app.schema.assistance import AssistanceSchema
from app.schema.request import RequestSchema, UserNeedsSchema
from app.db.database import get_db
from sqlalchemy.orm import Session

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.get("/{user_id}/needs", status_code=status.HTTP_200_OK, response_model=List[UserNeedsSchema])
def get_need(db: Session = Depends(get_db), user_id=int):
    needs = db.query(Request).filter(Request.user_id == user_id).all()
    return needs
