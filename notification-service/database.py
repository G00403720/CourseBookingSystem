import os, time 
from sqlalchemy import create_engine 
from sqlalchemy.ext.asyncio import async_sessionmaker 
from sqlalchemy.exc import OperationalError 

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true" 
RETRIES = int(os.getenv("DB_RETRIES", "10")) 
DELAY = float(os.getenv("DB_RETRY_DELAY", "1.5")) 

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else{}

engine = create_engine(DATABASE_URL, echo = True, connect_args=connect_args)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

for _ in range(RETRIES): 
    try: 
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=SQL_ECHO, 
connect_args=connect_args) 
        with engine.connect():  
            pass 
        break 
    except OperationalError: 
        time.sleep(DELAY) 
 
AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, 
expire_on_commit=False) 
 
