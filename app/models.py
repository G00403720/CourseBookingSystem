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
    courses: Mapped[list["Coursedb"]] = relationship(back_populates="owner", cascade="all, delete-orphan")

#Course database
class Coursedb(Base): 
    __tablename__ = "courses" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    code: Mapped[str] = mapped_column(unique=True)           
    name: Mapped[str] = mapped_column(nullable=False)          
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped["Userdb"] = relationship(back_populates="courses")  