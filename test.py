from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import model

# Create tables
model.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CUSTOMER API
# =========================

@app.post("/customers")
def create_customer(
    name: str,
    email: str,
    phone: int,
    city: str,
    db: Session = Depends(get_db)
):
    customer = model.CUSTOMER(
        name=name,
        email=email,
        phone=phone,
        city=city
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(model.CUSTOMER).all()
    return customers


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(model.CUSTOMER).filter(
        model.CUSTOMER.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@app.put("/customers/{customer_id}")
def update_customer(
    customer_id: int,
    name: str,
    city: str,
    db: Session = Depends(get_db)
):
    customer = db.query(model.CUSTOMER).filter(
        model.CUSTOMER.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.name = name
    customer.city = city

    db.commit()
    db.refresh(customer)

    return customer


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(model.CUSTOMER).filter(
        model.CUSTOMER.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted successfully"}


# =========================
# ORDERS API
# =========================

@app.post("/orders")
def create_order(
    productname: str,
    quantity: int,
    price: int,
    customer_id: int,
    db: Session = Depends(get_db)
):
    order = model.ORDERS(
        productname=productname,
        quantity=quantity,
        price=price,
        customer_id=customer_id
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(model.ORDERS).all()
    return orders


# =========================
# ADDRESS API
# =========================

@app.post("/address")
def create_address(
    street: str,
    state: str,
    pincode: int,
    customer_id: int,
    db: Session = Depends(get_db)
):
    address = model.ADDRESSTABLE(
        street=street,
        state=state,
        pincode=pincode,
        customer_id=customer_id
    )

    db.add(address)
    db.commit()
    db.refresh(address)

    return address


@app.get("/address")
def get_address(db: Session = Depends(get_db)):
    address = db.query(model.ADDRESSTABLE).all()
    return address


# =========================
# AUTH API
# =========================

@app.post("/register")
def register(
    name: str,
    email: str,
    password: str,
    role: str,
    db: Session = Depends(get_db)
):
    user = model.AUTH(
        name=name,
        email=email,
        password=password,
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(model.AUTH).all()
    return users