from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas
from ..utils import verify_token

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_task(task: schemas.TaskBase, db: Session = Depends(get_db), user=Depends(verify_token)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/")
def get_tasks(db: Session = Depends(get_db), user=Depends(verify_token)):
    return db.query(models.Task).all()


@router.put("/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db), user=Depends(verify_token)):
    task = db.query(models.Task).get(task_id)
    task.completed = True
    db.commit()
    return {"message": "Task marked as completed"}
