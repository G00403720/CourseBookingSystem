from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, selectinload 
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError 
import httpx

from database import engine, SessionLocal 
from models import Base, Coursedb
from schemas import CourseCreate, CourseRead
    
app = FastAPI() 
Base.metadata.create_all(bind=engine) 
USER_SERVICE_URL = "http://user-service:8000/users/"

def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() 

def commit_or_rollback(db: Session, error_msg: str): 
    try: 
        db.commit() 
    except IntegrityError: 
        db.rollback() 
        raise HTTPException(status_code=409, detail=error_msg)
      
@app.get("/health") 
def health(): 
    return {"status": "Course Service ok"}

async def validate_user_exists(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}{user_id}")

    if response.status_code != 200:
        raise HTTPException(status_code=409, detail="User not found")    

@app.post("/api/courses", response_model=CourseRead, status_code=201) 
async def create_course(course: CourseCreate, db: Session = Depends(get_db)):

    await validate_user_exists(course.owner_id) 

    cour = Coursedb( 
        name=course.name, 
        code=course.code, 
        owner_id=course.owner_id, 
    ) 
    db.add(cour) 
    commit_or_rollback(db, "Course creation failed") 
    db.refresh(cour) 
    return cour 
 
@app.get("/api/courses", response_model=list[CourseRead]) 
def list_courses(db: Session = Depends(get_db)): 
    stmt = select(Coursedb).order_by(Coursedb.id) 
    return db.execute(stmt).scalars().all() 
 
@app.get("/api/courses/{course_id}", response_model=CourseReadWithOwner) 
def get_course_with_owner(course_id: int, db: Session = Depends(get_db)): 
    stmt = select(Coursedb).where(Coursedb.id == course_id).options(selectinload(Coursedb.owner)) 
    cour = db.execute(stmt).scalar_one_or_none() 
    if not cour: 
        raise HTTPException(status_code=404, detail="Course not found") 
    return cour