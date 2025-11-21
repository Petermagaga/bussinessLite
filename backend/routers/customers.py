from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas
from ..utils import verify_token

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_customer(cus: schemas.CustomerBase, db: Session = Depends(get_db), user=Depends(verify_token)):
    new_cus = models.Customer(**cus.dict())
    db.add(new_cus)
    db.commit()
    db.refresh(new_cus)
    return new_cus


@router.get("/")
def get_customers(db: Session = Depends(get_db), user=Depends(verify_token)):
    return db.query(models.Customer).all()
