from pydantic import BaseModel

class NotificationCreate(BaseModel): 
    user_id: int
    message: str

class NotificationRead(BaseModel):  
    id: int 
    user_id: int
    message: str