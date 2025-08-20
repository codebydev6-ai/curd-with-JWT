from pydantic import BaseModel,EmailStr
from typing import Optional

class User(BaseModel):
    name : str
    email: EmailStr
    password : str
    address : str
    phone : str
    complete : Optional[bool] = False
    