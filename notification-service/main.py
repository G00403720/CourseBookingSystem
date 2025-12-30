from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError 

from database import engine, AsyncSessionLocal 
from models import Base, notificationdb
from schemas import NotificationCreate, NotificationRead
    
app = FastAPI() 
@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)

async def get_db(): 
    db = AsyncSessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() 

async def commit_or_rollback(db: AsyncSession, error_msg: str): 
    try: 
        db.commit() 
    except IntegrityError: 
        db.rollback() 
        raise HTTPException(status_code=409, detail=error_msg)
      
@app.get("/health") 
def health(): 
    return {"status": "Notification Service ok"}

@app.get("/api/notifications", response_model=list[NotificationRead])
async def list_notifications(db: AsyncSession = Depends(get_db)):
    stmt = select(notificationdb).order_by(notificationdb.id) 
    result = db.execute(stmt) 
    notifications = result.scalars().all() 
    return notifications

@app.get("/api/notifications/{user_id}", response_model=NotificationRead) 
def get_user(user_id: int, db: AsyncSession = Depends(get_db)): 
    user = db.get(notificationdb, user_id) 
    if not user: 
        raise HTTPException(status_code=404, detail="Notification not found") 
    return user 

@app.post("/api/notifications", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
async def add_notification(user_id: int, message: str, db: AsyncSession = Depends(get_db)):
    notification = notificationdb(user_id, message=message)
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification

@app.delete("/api/users/{user_id}", status_code=204) 
def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> Response: 
    notification = db.get(notificationdb, user_id) 
    if not notification: 
        raise HTTPException(status_code=404, detail="Notification not found") 
    db.delete(notification)          
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT) 