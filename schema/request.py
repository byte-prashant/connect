from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel
from schema.users import UserSchema
from schema.request_type import RequestTypeSchema
from pydantic import Required

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

class ResponseHelpSchema(BaseModel):

    reference_no: str
    msg: str

    class Config:
        orm_mode = True