from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from bizpilot.database import SessionLocal
from bizpilot.models.customer import Customer
from bizpilot.models.task import Task
from bizpilot.models.user import User
from bizpilot.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def get_stats(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()

    total_customers = db.query(Customer).filter(Customer.owner_id == user.id).count()
    total_tasks = db.query(Task).filter(Task.owner_id == user.id).count()
    completed_tasks = db.query(Task).filter(Task.owner_id == user.id, Task.completed == True).count()
    pending_tasks = db.query(Task).filter(Task.owner_id == user.id, Task.completed == False).count()

    return {
        "total_customers": total_customers,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    }

@router.get("/customers-per-month")
def customers_per_month(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()

    rows = db.query(
        extract('month', Customer.id).label("month"),
        func.count(Customer.id)
    ).filter(Customer.owner_id == user.id).group_by("month").all()

    result = [{"month": int(month), "count": count} for month, count in rows]
    return result


@router.get("/tasks-completed-per-month")
def tasks_completed_per_month(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()

    rows = db.query(
        extract('month', Task.updated_at).label("month"),
        func.count(Task.id)
    ).filter(Task.owner_id == user.id, Task.completed == True).group_by("month").all()

    result = [{"month": int(month), "count": count} for month, count in rows]
    return result

@router.get("/recent-tasks")
def recent_tasks(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user).first()

    tasks = (
        db.query(Task)
        .filter(Task.owner_id == user.id)
        .order_by(Task.created_at.desc())
        .limit(5)
        .all()
    )

    return [
        {
            "id": t.id,
            "title": t.title,
            "completed": t.completed,
            "created_at": t.created_at,
        }
        for t in tasks
    ]
