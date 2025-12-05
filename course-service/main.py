from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError 

from database import engine, SessionLocal 
from models import Base, Coursedb
from schemas import CourseCreate, CourseRead
    
app = FastAPI() 
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

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

@app.get("/api/courses", response_model=list[CourseRead]) 
def list_courses(db: Session = Depends(get_db)): 
    stmt = select(Coursedb).order_by(Coursedb.id) 
    result = db.execute(stmt) 
    courses = result.scalars().all() 
    return courses 
    
@app.get("/api/courses/{course_id}", response_model=CourseRead) 
def get_course(course_id: int, db: Session = Depends(get_db)): 
    course = db.get(Coursedb, course_id) 
    if not course: 
        raise HTTPException(status_code=404, detail="Course not found") 
    return course 
 
@app.post("/api/courses", response_model=CourseRead, status_code=status.HTTP_201_CREATED) 
def add_course(payload: CourseCreate, db: Session = Depends(get_db)): 
    course = Coursedb(**payload.model_dump()) 
    db.add(course) 
    try: 
        db.commit() 
        db.refresh(course) 
    except IntegrityError: 
        db.rollback() 
        raise HTTPException(status_code=409, detail="Course already exists") 
    return course 

@app.delete("/api/courses/{course_id}", status_code=204) 
def delete_course(course_id: int, db: Session = Depends(get_db)) -> Response: 
    course = db.get(Coursedb, course_id) 
    if not course: 
        raise HTTPException(status_code=404, detail="Course not found") 
    db.delete(course)          
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT) 