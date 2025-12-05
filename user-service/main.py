from fastapi import FastAPI, Depends, HTTPException, status, Response 
from sqlalchemy.orm import Session 
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError 

from database import engine, SessionLocal 
from models import Base, Userdb
from schemas import UserCreate, UserRead
    
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
    return {"status": "User Service ok"}

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

@app.delete("/api/users/{user_id}", status_code=204) 
def delete_user(user_id: int, db: Session = Depends(get_db)) -> Response: 
    user = db.get(Userdb, user_id) 
    if not user: 
        raise HTTPException(status_code=404, detail="User not found") 
    db.delete(user)          
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT) 


