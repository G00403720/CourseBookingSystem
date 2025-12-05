from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base,  Mapped, mapped_column

#Creates base class for table
Base = declarative_base()

#Booking database
class Bookingdb(Base): 
    __tablename__ = "bookings" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    user_id: Mapped[int] = mapped_column(Integer, nullable=False) 
    user_name :  Mapped[str] = mapped_column(String(100), nullable=False) 
    user_age: Mapped[int] = mapped_column(Integer, nullable=False)
    user_email : Mapped[str] = mapped_column(unique=True, nullable=False)    
    course_id: Mapped[int] = mapped_column(Integer, nullable=False)
    course_name: Mapped[str] = mapped_column(String, nullable=False)    
    course_code: Mapped[str] = mapped_column(unique=True)           
     