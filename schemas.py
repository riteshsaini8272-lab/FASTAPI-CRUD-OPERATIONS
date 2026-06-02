from pydantic import BaseModel,EmailStr
#CUSROMerTABLE
class CUSTOMER(BaseModel):
    name:str
    email:EmailStr  
    phone:int 
    city:str 
#ORDERS TABLE
class ORDER(BaseModel):   
    id:int
    productname:str
    quantity:int
    price:int
#ADDRESS TABLE
class ADDRESS(BaseModel):
    street:str
    state:str
    pincode:int
#AUTH TABLE
class AUTHS(BaseModel):
    name:str
    email:str
    password:str
    role:str