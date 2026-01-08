from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class UserCreate(BaseModel):
    username : str
    password:str
    name: str
    email: Optional[str]
    user_type: str
    created_at : datetime

class UserResponse(BaseModel):
    user_id : str
    username : str
    name: str
    email: Optional[str]
    user_type: str
    created_at : datetime


