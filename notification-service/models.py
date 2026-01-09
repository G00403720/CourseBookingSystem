from sqlalchemy import String, Integer
from sqlalchemy.orm import declarative_base,  Mapped, mapped_column

#Creates base class for table
Base = declarative_base()

#Notification database
class Notificationdb(Base): 
    __tablename__ = "notifications" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    user_id: Mapped[int] = mapped_column(Integer, nullable=False) 
    message: Mapped[str] = mapped_column(String, nullable=False)           
             