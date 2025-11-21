from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from bizpilot.database import SessionLocal
from bizpilot.models.task import Task
from bizpilot.models.customer import Customer
from bizpilot.models.user import User
from bizpilot.schemas.task_schema import TaskCreate, TaskOut, TaskUpdate
from bizpilot.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a task
@router.post("/", response_model=TaskOut)
def create_task(data: TaskCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()

    # Check if the customer belongs to this user
    customer = db.query(Customer).filter(Customer.id == data.customer_id, Customer.owner_id == owner.id).first()
    if not customer:
        raise HTTPException(404, "Customer not found or not yours")

    task = Task(
        title=data.title,
        description=data.description,
        customer_id=data.customer_id,
        owner_id=owner.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# List all tasks
@router.get("/", response_model=list[TaskOut])
def list_tasks(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()
    tasks = db.query(Task).filter(Task.owner_id == owner.id).all()
    return tasks

# Get one task
@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner.id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    return task

# Update a task
@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()

    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner.id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.completed is not None:
        task.completed = data.completed

    db.commit()
    db.refresh(task)
    return task

# Delete task
@router.delete("/{task_id}")
def delete_task(task_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()

    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner.id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
