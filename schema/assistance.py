from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel
from schema.users import UserSchema
from schema.request_type import RequestTypeSchema
from schema.request import RequestSchema
from pydantic import Required

class AssistanceSchema(BaseModel):

    id: int
    request: Union[RequestSchema]
    request_id: int
    user_id: int
    saint: Union[UserSchema]
    is_active: bool
    seeker_lat: Required[str]
    seeker_lon: Required[str]

    class Config:
        orm_mode = True
