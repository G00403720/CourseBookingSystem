from pydantic import BaseModel, StringConstraints
from typing import Annotated

CourseNameStr  = Annotated[str, StringConstraints(min_length=1, max_length=255)] 
CodeStr        = Annotated[str, StringConstraints(min_length=1, max_length=32)] 

class CourseCreate(BaseModel): 
    name: CourseNameStr 
    code: CodeStr 

class CourseRead(BaseModel):  
    id: int 
    name: CourseNameStr
    code: CodeStr
    