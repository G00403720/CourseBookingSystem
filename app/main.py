from fastapi import FastAPI, Depends, HTTPException, status, Response 
from sqlalchemy.orm import Session 
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.orm import selectinload 
from .database import engine, SessionLocal 
from .models import Base, Userdb, Coursedb
from .schemas import ( 
    UserCreate, UserRead, 
    CourseCreate, CourseRead,  
    CourseReadWithOwner, CourseCreateForUser 
) 

app = FastAPI() 
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
    return {"status": "ok"} 

#Courses
@app.post("/api/courses", response_model=CourseRead, status_code=201) 
def create_course(course: CourseCreate, db: Session = Depends(get_db)): 
    user = db.get(Userdb, course.owner_id) 
    if not user: 
        raise HTTPException(status_code=404, detail="User not found") 
 
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
 
#Nested Routes 
@app.get("/api/users/{user_id}/courses", response_model=list[CourseRead]) 
def get_user_courses(user_id: int, db: Session = Depends(get_db)): 
    stmt = select(Coursedb).where(Coursedb.owner_id == user_id) 
    result = db.execute(stmt) 
    rows = result.scalars().all() 
    return rows 
     
#Users
@app.post("/api/users/{user_id}/courses", response_model=CourseRead, status_code=201) 
def create_user_course(user_id: int, course: CourseCreateForUser, db: Session = 
Depends(get_db)): 
    user = db.get(Userdb, user_id) 
    if not user: 
        raise HTTPException(status_code=404, detail="User not found") 
 
    cour = Coursedb( 
        name=course.name, 
        code=course.code,   
        owner_id=user_id 
    ) 
    db.add(cour) 
    commit_or_rollback(db, "Course creation failed") 
    db.refresh(cour) 
    return cour 
 
@app.get("/api/users", response_model=list[UserRead]) 
def list_users(db: Session = Depends(get_db)): 
    stmt = select(Userdb).order_by(Userdb.id) 
    result = db.execute(stmt) 
    users = result.scalars().all() 
    return users 
    
 
@app.get("/api/users/{user_id}", response_model=UserRead) 
def get_user(user_id: int, db: Session = Depends(get_db)): 
    user = db.get(Userdb, user_id) 
    if not user: 
        raise HTTPException(status_code=404, detail="User not found") 
    return user 
 
@app.post("/api/users", response_model=UserRead, status_code=status.HTTP_201_CREATED) 
def add_user(payload: UserCreate, db: Session = Depends(get_db)): 
    user = Userdb(**payload.model_dump()) 
    db.add(user) 
    try: 
        db.commit() 
        db.refresh(user) 
    except IntegrityError: 
        db.rollback() 
        raise HTTPException(status_code=409, detail="User already exists") 
    return user 
 
# DELETE a user (triggers ORM cascade -> deletes their courses too) 
@app.delete("/api/users/{user_id}", status_code=204) 
def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response: 
    user = db.get(Userdb, user_id) 
    if not user: 
        raise HTTPException(status_code=404, detail="User not found") 
    db.delete(user)          
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

