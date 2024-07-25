from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from typing import List

import json
import aiofiles

from db import db_connection
from model.models import DBConnection, Address, InputAddress

import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
def redirect_index():
    return "static/index.html"

@app.get("/index", response_class=FileResponse)
def index():
    return "static/index.html"

@app.get("/connect", response_class=FileResponse)
def connect():
    return "static/html/connect.html"

@app.get('/hcheck')
def hcheck():
    return "OK"

@app.post("/connect_to_db")
async def connect_to_db(dbConnection: DBConnection):
    data = json.dumps(dbConnection.dict()).encode('utf-8')

    async with aiofiles.open('static/db_connection.config', 'wb') as out_file:
        await out_file.write(data)  # async write chunk

    db_connection.make_table()

    return {"Result": "OK"}

@app.post("/address/add")
def add_todo(address: InputAddress):
    logger.debug('this is a debug message')
    db_connection.add_todo(address)

@app.get("/address/read", response_model=List[Address])
def read_todo():
    return db_connection.read_todo()

@app.post("/address/update")
def update_todo(address: Address):
    db_connection.update_todo(address)

