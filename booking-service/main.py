from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError 

from database import engine, SessionLocal 
from models import Base, Bookingdb
from schemas import BookingCreate, BookingRead

import requests
    
USER_SERVICE_URL = "http://user-service:8000"
COURSE_SERVICE_URL = "http://course-service:8000"  

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
    return {"status": "Booking Service ok"}

def validate_user(user_id: int):
    Response = requests.get(f"{USER_SERVICE_URL}/api/users/{user_id}")
    if Response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")
    return Response.json()

def validate_course(course_id: int):
    Response = requests.get(f"{COURSE_SERVICE_URL}/api/courses/{course_id}")
    if Response.status_code != 200:
        raise HTTPException(status_code=404, detail="Course not found")    
    return Response.json()

@app.get("/api/bookings", response_model=list[BookingRead]) 
def list_bookings(db: Session = Depends(get_db)): 
    stmt = select(Bookingdb).order_by(Bookingdb.id) 
    result = db.execute(stmt) 
    bookings = result.scalars().all() 
    return bookings 
    
@app.get("/api/bookings/{booking_id}", response_model=BookingRead) 
def get_booking(booking_id: int, db: Session = Depends(get_db)): 
    booking = db.get(Bookingdb, booking_id) 
    if not booking: 
        raise HTTPException(status_code=404, detail="booking not found") 
    return booking 
 
@app.post("/api/bookings", response_model=BookingRead, status_code=status.HTTP_201_CREATED) 
def add_booking(payload: BookingCreate, db: Session = Depends(get_db)): 
    user = validate_user(payload.user_id)
    course = validate_course(payload.course_id)

    booking_data = {
        "user_id": user["id"],
        "user_name": user["name"],
        "user_age": user["age"],
        "user_email": user["email"],
        "course_id": course["id"],
        "course_name": course["name"],
        "course_code": course["code"]
    }
    booking = Bookingdb(**booking_data) 
    db.add(booking) 
    try: 
        db.commit() 
        db.refresh(booking) 
    except IntegrityError: 
        db.rollback() 
        raise HTTPException(status_code=409, detail="booking already exists") 
    
    requests.post(
        "http://notification-service:8005/api/notifications",
        params={
            "user_id": payload.user_id,
            "message": "Booking successfully created"
        }
    )
    return booking 

@app.delete("/api/bookings/{booking_id}", status_code=204) 
def delete_booking(booking_id: int, db: Session = Depends(get_db)) -> Response: 
    booking = db.get(Bookingdb, booking_id) 
    if not booking: 
        raise HTTPException(status_code=404, detail="booking not found") 
    db.delete(booking)          
    db.commit()

    user_id = booking.user_id 

    requests.post(
        "http://notification-service:8005/api/notifications",
        params={
            "user_id": user_id,
            "message": "Booking successfully deleted"
        }
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT) 