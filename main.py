from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from api.users import user_router
from api.request_type import requirement_router

load_dotenv('.env')
app = FastAPI()
app.include_router(user_router)
app.include_router(requirement_router)
