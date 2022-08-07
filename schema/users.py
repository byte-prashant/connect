from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel
#from schema.request import RequestSchema
from pydantic import Required

class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    # request: Union[RequestSchema]
    # assisance: Union[RequestSchema]
    hashed_password: str
    is_active: bool

    class Config:
        orm_mode = True

class RequestUserSchema(BaseModel):

    email: str
    name: str
    phone: str

    class Config:
        orm_mode = True


class ResponseUserSchema(RequestUserSchema):
   pass

