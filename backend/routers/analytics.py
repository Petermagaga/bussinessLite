from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..utils import verify_token
from .. import models

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_dashboard(db: Session = Depends(get_db), user=Depends(verify_token)):
    total_customers = db.query(models.Customer).count()
    total_tasks = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.completed == True).count()

    return {
        "total_customers": total_customers,
        "total_tasks": total_tasks,
        "completed_tasks": completed,
        "pending_tasks": total_tasks - completed,
    }
