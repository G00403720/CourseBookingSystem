from pydantic import BaseModel, EmailStr,  StringConstraints
from typing import Annotated, Optional, List 
from annotated_types import Ge, Le 

NameStr        = Annotated[str, StringConstraints(min_length=1, max_length=100)]
CourseNameStr  = Annotated[str, StringConstraints(min_length=1, max_length=255)] 
CodeStr        = Annotated[str, StringConstraints(min_length=1, max_length=32)] 
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

class CourseCreate(BaseModel): 
    name: CourseNameStr 
    code: CodeStr 
    owner_id: int

class CourseRead(CourseCreate):  
    id: int 
    name: CourseNameStr
    owner_id: int

class UserReadWithCourses(UserRead): 
    Courses: List[CourseRead] = [] 

class CourseCreateForUser(BaseModel): 
    name: CourseNameStr 
    code: CodeStr

class CourseReadWithOwner(CourseRead): 
    owner: Optional["UserRead"] = None