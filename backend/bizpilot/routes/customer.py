from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from bizpilot.database import SessionLocal
from bizpilot.models.customer import Customer
from bizpilot.models.user import User
from bizpilot.schemas.customer_schema import CustomerCreate, CustomerOut, CustomerUpdate
from bizpilot.auth.jwt_handler import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create customer
@router.post("/", response_model=CustomerOut)
def create_customer(data: CustomerCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()

    customer = Customer(
        name=data.name,
        email=data.email,
        phone=data.phone,
        address=data.address,
        owner_id=owner.id
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

# List all customers
@router.get("/", response_model=list[CustomerOut])
def list_customers(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()
    customers = db.query(Customer).filter(Customer.owner_id == owner.id).all()
    return customers

# Get single customer
@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()
    customer = db.query(Customer).filter(Customer.id == customer_id, Customer.owner_id == owner.id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Update customer
@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, data: CustomerUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):

    owner = db.query(User).filter(User.username == current_user).first()
    customer = db.query(Customer).filter(Customer.id == customer_id, Customer.owner_id == owner.id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.name = data.name
    customer.email = data.email
    customer.phone = data.phone
    customer.address = data.address

    db.commit()
    db.refresh(customer)
    return customer

# Delete customer
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    owner = db.query(User).filter(User.username == current_user).first()
    customer = db.query(Customer).filter(Customer.id == customer_id, Customer.owner_id == owner.id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}
