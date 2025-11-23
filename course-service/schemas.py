from pydantic import BaseModel, StringConstraints
from typing import Annotated, Optional, List 

CourseNameStr  = Annotated[str, StringConstraints(min_length=1, max_length=255)] 
CodeStr        = Annotated[str, StringConstraints(min_length=1, max_length=32)] 

class CourseCreate(BaseModel): 
    name: CourseNameStr 
    code: CodeStr 
    owner_id: int

class CourseRead(CourseCreate):  
    id: int 
    name: CourseNameStr
    owner_id: int