from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str

class CustomerOut(CustomerBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: str
    customer_id: int

class TaskOut(TaskBase):
    id: int
    completed: bool
    class Config:
        orm_mode = True
