from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(Integer, unique=True)
    city = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    # Relationships
    orders = relationship("Order", back_populates="customer")
    addresses = relationship("Address", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    productname = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_created = Column(DateTime, default=func.now())
    # Relationship
    customer = relationship("Customer", back_populates="orders")
class Address(Base):
    __tablename__ = "address"
    id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    street = Column(String(255))
    state = Column(String(255))
    pincode = Column(Integer)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    # Relationship
    customer = relationship("Customer", back_populates="addresses")


class Auth(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    role = Column(String(50))