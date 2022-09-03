from typing import Optional, Union
from pydantic import BaseModel
from app.schema.users import UserSchema
from app.schema.request_type import RequestTypeSchema
from typing import List


class RequestSchema(BaseModel):

    id: int
    seeker: Union[UserSchema]
    request_type = Union[RequestTypeSchema]
    is_active:  bool
    lat: str
    long: str

    class Config:
        orm_mode = True


class RequestHelpSchema(BaseModel):

    request_type: int
    phone: Optional[str]
    lat: str
    long: str

    class Config:
        orm_mode = True

class CreateRequestSchema(RequestHelpSchema):

    reference_no: str
    user_id: int

    class Config:
        orm_mode = True


class ResponseHelpSchema(BaseModel):

    reference_no: str
    msg: str

    class Config:
        orm_mode = True


class SeekHelpSchema(BaseModel):
    id: str
    lat: str
    long: str
    req_type_id:int
    distance: float

    class Config:
        orm_mode = True

class CreateMultipleRequest(BaseModel):

    seeker = []

    class Config:
        orm_mode = True



