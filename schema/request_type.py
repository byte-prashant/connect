from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pydantic import Required


class RequestTypeSchema(BaseModel):

    id: int
    name: str
    is_active: bool


class RequirementTypeSchema(BaseModel):
    name: str


class ResposnseRequirementTypeSchema(BaseModel):
    name: str



