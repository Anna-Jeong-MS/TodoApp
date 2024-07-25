from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DBConnection(BaseModel):
    serverName: str
    admin: str
    password: str

class Address(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    gender: str
    ip_address: str

class InputAddress(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: str
    ip_address: str