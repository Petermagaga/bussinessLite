from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from bizpilot.database import SessionLocal
from bizpilot.models.user import User
from bizpilot.schemas.user_schema import UserCreate, UserLogin, UserOut
from bizpilot.auth.hash import hash_password, verify_password
from bizpilot.auth.jwt_handler import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.username == user.username).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Username already exists")

    email_exist = db.query(User).filter(User.email == user.email).first()
    if email_exist:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(user.password)

    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# Login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access = create_access_token({"sub": db_user.username})
    refresh = create_refresh_token({"sub": db_user.username})

    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
