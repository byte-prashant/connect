
from typing import List
from fastapi import APIRouter, Depends, status
from  app.models.assistance import Assistance
from app.schema.assistance import AssistanceSchema
from app.db.database import get_db
from sqlalchemy.orm import Session
assist_router = APIRouter(prefix="/assists", tags=["Assistance"])


@assist_router.get("/{need_id}", status_code=status.HTTP_200_OK, response_model=List[AssistanceSchema])
def get_assistance(db: Session = Depends(get_db), need_id=int):
    assists = db.query(Assistance).filter(Assistance.request_id == need_id).all()
    return assists



