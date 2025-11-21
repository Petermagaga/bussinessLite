from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from bizpilot.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String)

    # Relationship: user who created this customer
    owner_id = Column(Integer, ForeignKey("users.id"))
