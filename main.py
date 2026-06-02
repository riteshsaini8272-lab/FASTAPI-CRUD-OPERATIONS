from fastapi import FastAPI,HTTPException,Depends,status
from sqlalchemy.orm import Session
import model
from typing import Optional
from pydantic import BaseModel,EmailStr
from sqlalchemy import func
from database import get_db

app = FastAPI()

class CUSTOMER(BaseModel):
    name:str
    email:EmailStr  
    phone:int 
    city:str 

class ADDRESS(BaseModel):
    street:str
    state:str
    pincode:int

@app.post("/ADD-CUSTOMER")
def add_customers(customer: CUSTOMER,addr: ADDRESS,db: Session = Depends(get_db)):
    existing_user = db.query(model.Customer).filter(model.Customer.email == customer.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already exists")
    users = model.Customer(name=customer.name,email=customer.email,phone=customer.phone,city=customer.city)
    db.add(users)
    db.commit()
    db.refresh(users)
    addres = model.Address(street=addr.street,state=addr.state,pincode=addr.pincode,customer_id=users.id)
    db.add(addres)
    db.commit()
    db.refresh(addres)
    return {
        "customer": {
            "id": users.id,
            "name": users.name,
            "email": users.email,
            "phone": users.phone,
            "city": users.city
        },
        "address": {
            "id": addres.id,
            "street": addres.street,
            "state": addres.state,
            "pincode": addres.pincode
        }
    }
class ORDER(BaseModel):   
    productname:str
    quantity:int
    price:int

@app.post("/ADD-ORDER/{customers_id}")
def add_order(customers_id:int,ode:ORDER,db:Session=Depends(get_db)):
    query=db.query(model.Customer).filter(model.Customer.id==customers_id,model.Customer.is_active==True).first()
    if query is None:
        raise HTTPException(status_code=402,detail="CUSTOMER NOT FOUND ")
    user_orders=model.Order(productname=ode.productname,quantity=ode.quantity,price=ode.price,customer_id=query.id)
    db.add(user_orders)
    db.commit()
    db.refresh(user_orders)
    return user_orders

@app.get("/SHOW-ORDER/{Customer_id}")
def get_order (Customer_id:int,db:Session=Depends(get_db)):
    query=db.query(model.Order).filter(model.Order.customer_id==Customer_id).first()
    return query

@app.get("/SHOW-CUSTOMERS")
def get_customer(db: Session = Depends(get_db)):
    users = db.query(model.Customer).filter(model.Customer.is_active == True).all()
    useradd = db.query(model.Address).all()
    userodd = db.query(model.Order).all()
    return {
        "customers": users,
        "addresses": useradd,
        "orders": userodd
    }
@app.get("/ADDRESS")
def get_address(db:Session=Depends(get_db)):
    query=db.query(model.Address).all()
    return query

@app.get("/SEARCH-CUSTOMER-BY(Name-Email-ID)")
def search_user(name:Optional[str]=None,email:Optional[str]=None,id:Optional[int]=None,db:Session=Depends(get_db)):
    query=db.query(model.Customer)
    if name is not None:
        query = query.filter(func.lower(model.Customer.name )== name.lower())
    if email is not None:
        query = query.filter(func.lower(model.Customer.email) == email.lower())
    if id is not None:
        query = query.filter(model.Customer.id == id)
    return query.all()

class UPDATECUSTOMER(BaseModel):
    name:str
    email:EmailStr  
    phone:int 
    city:str   

@app.put("/UPDATE-CUSTOMER/{customer_id}")
def update_customer(customer_id:int,custom:CUSTOMER,db:Session=Depends(get_db)):
    users=db.query(model.Customer).filter(model.Customer.id==customer_id,model.Customer.is_active==True).first()
    if users is None:
        raise HTTPException(status_code=403,detail="NO CUSTOMER PRESENT WITH THIS ID ")
    users.name=custom.name
    users.email=custom.email
    users.phone=custom.phone
    users.city=custom.city
    db.commit()
    db.refresh(users)
    return users

class UPDATEORDER(BaseModel):   
    productname:str
    quantity:int
    price:int

@app.put("/update-order/{order_id}")
def update_order(order_id: int, oddr: UPDATEORDER, db: Session = Depends(get_db)):
    order = db.query(model.Order).filter(model.Order.customer_id == order_id).first()
    if order is None:
        raise HTTPException(status_code=402,detail="NO ORDER WITH THIS ID")
    order.productname = oddr.productname
    order.quantity = oddr.quantity
    order.price = oddr.price
    db.commit()
    db.refresh(order)
    return order

@app.put("/update-address/{customer_id}")
def update_address(customer_id:int,addr:ADDRESS,db:Session=Depends(get_db)):
    address=db.query(model.Address).filter(model.Address.customer_id==customer_id).first()
    if address is None:
        raise HTTPException(status_code=402,detail="ADDRESS NOT FOUND")
    address.street=addr.street
    address.state=addr.state
    address.pincode=addr.pincode
    db.commit()
    db.refresh(address)
    return address
    
@app.delete("/SOFT.delete-customer/{id}")
def delete_customer(id:int,db:Session=Depends(get_db) ):
    user=db.query(model.Customer).filter(model.Customer.id==id,model.Customer.is_active==True).first()
    if user is None:
        raise HTTPException(status_code=402,detail="USER NOT FOUND")
    user.is_active=False
    db.commit()  
    return{"MESSAGE":"CUSTOMER DELETED"}

@app.put("/RESTORE-CUSTOMER/{id}")
def restore_customer(id:int,db:Session=Depends(get_db)):
    user=db.query(model.Customer).filter(model.Customer.id==id,model.Customer.is_active==False).first()
    if user is None:
        raise HTTPException(status_code=402,detail="USER NOT FOUND")
    user.is_active=True
    db.commit()
    db.refresh(user)
    return{"MESSAGE":"USER RESTORE"}
  
@app.delete("/DELETE-ORDER/{id}")
def delete_order(id:int,db:Session=Depends(get_db)):
    user=db.query(model.Order).filter(model.Order.customer_id==id).first()
    if user is None:
        raise HTTPException(status_code=402,detail="ORDER NOT FOUND")
    db.delete(user)
    db.commit()
    return{"MESSAGE":"ORDER DELETED"}

@app.delete("/DElETE-ADDRESS/{id}")
def delete_address(id:int,db:Session=Depends(get_db)):
    user=db.query(model.Address).filter(model.Address.customer_id==id).first()
    if user is None:
        raise HTTPException(status_code=402,detail="ADDRESS NOT FOUND")
    db.delete(user)
    db.commit()
    return{"MESSAGE":"ADDRESS DELETED"}