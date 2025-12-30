from pydantic import BaseModel

class NotificationCreate(BaseModel): 
    pass

class NotificationRead(BaseModel):  
    id: int 
    