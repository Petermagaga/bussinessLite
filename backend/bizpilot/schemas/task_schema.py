from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str
    customer_id: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    customer_id: int

    class Config:
        orm_mode = True
