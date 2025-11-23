from pydantic import BaseModel, EmailStr,  StringConstraints
from typing import Annotated 
from annotated_types import Ge, Le 

NameStr        = Annotated[str, StringConstraints(min_length=1, max_length=100)]
AgeInt         = Annotated[int, Ge(0), Le(150)] 

class UserCreate(BaseModel): 
    name: NameStr 
    email: EmailStr 
    age: AgeInt 

class UserRead(BaseModel):  
    id: int 
    name: NameStr 
    email: EmailStr 
    age: AgeInt 