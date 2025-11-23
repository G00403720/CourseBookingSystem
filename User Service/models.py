from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base,  Mapped, mapped_column, relationship

#Creates base class for table
Base = declarative_base()

#User database
class Userdb(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name :  Mapped[str] = mapped_column(String(100), nullable=False) 
    email : Mapped[str] = mapped_column(unique=True, nullable=False) 
    age: Mapped[int] = mapped_column(Integer, nullable=False)