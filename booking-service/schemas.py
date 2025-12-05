from pydantic import BaseModel, EmailStr,  StringConstraints
from typing import Annotated 
from annotated_types import Ge, Le 

NameStr        = Annotated[str, StringConstraints(min_length=1, max_length=100)]
AgeInt         = Annotated[int, Ge(0), Le(150)] 
CourseNameStr  = Annotated[str, StringConstraints(min_length=1, max_length=255)] 
CodeStr        = Annotated[str, StringConstraints(min_length=1, max_length=32)] 

class BookingCreate(BaseModel): 
    user_id: int
    course_id: int

class BookingRead(BaseModel):  
    id: int
    user_id: int
    user_name: NameStr 
    user_age: AgeInt 
    user_email: EmailStr
    course_id: int
    course_name: CourseNameStr
    course_code: CodeStr