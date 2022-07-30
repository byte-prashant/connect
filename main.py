from typing import Union

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware, db
import os
load_dotenv('.env')
app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}