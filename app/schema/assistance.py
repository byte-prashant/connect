
from pydantic import BaseModel
from pydantic import Required
from typing import Optional


class AssistanceSchema(BaseModel):

    request_id: int
    user_id: int
    lat: str
    long: str

    class Config:
        orm_mode = True


class RequestAssistanceSchema(BaseModel):

    request_id: int
    user_id: Optional[int]
    lat: str
    long: str

    class Config:
        orm_mode = True


class CreateAssistanceSchema(BaseModel):

    lat: str
    long: str

    class Config:
        orm_mode = True