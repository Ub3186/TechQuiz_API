from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username:str
    email:str
    password:str
    admin:Optional[bool] = False
    score:Optional[int] = 0
    createdAt:Optional[datetime] = datetime.now()
    friends:Optional[list] = []

class UpdateUser(BaseModel):
    username:Optional[str] = None
    email:Optional[str] = None
    password:Optional[str] = None

class Question(BaseModel):
    type:str
    question:str
    option1:str
    option2:str
    option3:str
    option4:str
    answer:str

class UpdatePassword(BaseModel):
    email:str
    password:str