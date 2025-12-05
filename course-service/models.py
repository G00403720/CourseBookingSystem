from sqlalchemy import String
from sqlalchemy.orm import declarative_base,  Mapped, mapped_column

#Creates base class for table
Base = declarative_base()

#Course database
class Coursedb(Base): 
    __tablename__ = "courses" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String, nullable=False) 
    code: Mapped[str] = mapped_column(unique=True)           
             