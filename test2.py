from fastapi import FastAPI, Depends
from database import get_db, engine
from pydantic import BaseModel
from sqlalchemy.orm import Session
import model
from typing import Optional

app = FastAPI()

# EMPLOYEE SCHEMA
class EMPLOYEE(BaseModel):
    name: str
    age: int
    address: str
    phone: int
    email: str
    password: str

# TASK SCHEMA
class TASK(BaseModel):
    task_name: str

# CREATE EMPLOYEE
@app.post("/employee")
def add_employee(book: EMPLOYEE,db: Session = Depends(get_db)):
    new_employee = model.EMP(
        name=book.name,
        age=book.age,
        address=book.address,
        phone=book.phone,
        email=book.email,
        password=book.password
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# CREATE TASK
@app.post("/task/{employee_id}")
def add_task(task: TASK,employee_id: int,db: Session = Depends(get_db)):
    employee = db.query(model.EMP).filter(model.EMP.id == employee_id,model.EMP.is_deleted == False).first()
    if employee is None:
        return {"MESSAGE": "EMPLOYEE NOT FOUND"}

    new_task = model.TAS(Task_name=task.task_name,employee_id=employee_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# GET EMPLOYEE
@app.get("/get_employee")
def get_employee(db: Session = Depends(get_db)):
    employee = db.query(model.EMP).filter(model.EMP.is_deleted == False).all()
    
    return employee

# GET EMPLOYEE by id
@app.get("/get_employee_BYID/{employee_id}")
def get_employee(employee_id:int,db: Session = Depends(get_db)):
    employee = db.query(model.EMP).filter(model.EMP.id==employee_id,model.EMP.is_deleted == False).first()
    return employee
# GET TASK
@app.get("/get_task")
def get_task(db: Session = Depends(get_db)):
    tasks = db.query(model.TAS).all()
    return tasks

# SOFT DELETE
@app.delete("/delete/{employee_id}")
def delete_employee(employee_id: int,db: Session = Depends(get_db)):

    employee = db.query(model.EMP).filter(model.EMP.id == employee_id,model.EMP.is_deleted == False).first()
    if employee is None:
        return {"MESSAGE": "EMPLOYEE NOT FOUND"}
    employee.is_deleted = True
    db.commit()
    return {"MESSAGE": "EMPLOYEE DELETED"}

# PERMANent DELETE
@app.delete("/Pdelete/{employee_id}")
def delete_employee(employee_id: int,db: Session = Depends(get_db)):

    employee = db.query(model.EMP).filter(model.EMP.id == employee_id).first()
    if employee is None:
        return {"MESSAGE": "EMPLOYEE NOT FOUND"}
    db.delete(employee)     
    db.commit()

    return {"MESSAGE": "EMPLOYEE DELETED"}
# PUT SCHEMA
class EmployeeUpdate(BaseModel):
    name: str
    age: int
    address: str
    phone: int
    email: str
    password: str

# PATCH SCHEMA
class EmployeePatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[int] = None
    email: Optional[str] = None
    password: Optional[str] = None

# UPDATE EMPLOYEE
@app.put("/update/{employee_id}")
def update_employee(employee_id: int,updated_employee: EmployeeUpdate,db: Session = Depends(get_db)):

    employee = db.query(model.EMP).filter(model.EMP.id == employee_id).first()
    if employee is None:
        return {"MESSAGE": "EMPLOYEE NOT FOUND"}
    employee.name = updated_employee.name
    employee.age = updated_employee.age
    employee.address = updated_employee.address
    employee.phone = updated_employee.phone
    employee.email = updated_employee.email
    employee.password = updated_employee.password
    db.commit()
    db.refresh(employee)
    return employee

# PATCH EMPLOYEE
@app.patch("/patch/{employee_id}")
def patch_employee(employee_id: int,patched_employee: EmployeePatch,db: Session = Depends(get_db)):
    employee = db.query(model.EMP).filter(model.EMP.id == employee_id).first()
    if employee is None:
        return {"MESSAGE": "EMPLOYEE NOT FOUND"}

    if patched_employee.name is not None:
        employee.name = patched_employee.name

    if patched_employee.age is not None:
        employee.age = patched_employee.age

    if patched_employee.address is not None:
        employee.address = patched_employee.address

    if patched_employee.phone is not None:
        employee.phone = patched_employee.phone

    if patched_employee.email is not None:
        employee.email = patched_employee.email

    if patched_employee.password is not None:
        employee.password = patched_employee.password

    db.commit()
    db.refresh(employee)
    return employee

# RESTORE EMPLOYEE
@app.put("/restore/{employee_id}")
def restore_employee(employee_id: int,db: Session = Depends(get_db)):
    employee = db.query(model.EMP).filter(model.EMP.id == employee_id,model.EMP.is_deleted == True).first()
    if employee is None:
        return {"MESSAGE": "EMPLOYEE NOT FOUND"}
    employee.is_deleted = False
    db.commit()
    return {"MESSAGE": "EMPLOYEE RESTORED"}