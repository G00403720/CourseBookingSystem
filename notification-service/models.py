from sqlalchemy import String
from sqlalchemy.orm import declarative_base,  Mapped, mapped_column

#Creates base class for table
Base = declarative_base()

#Notification database
class notificationdb(Base): 
    __tablename__ = "notifications" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    user_id: Mapped[str] = mapped_column(String, nullable=False) 
    message: Mapped[str] = mapped_column(unique=True)           
             