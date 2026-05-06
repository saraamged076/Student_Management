from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import models
from app.routers.routers import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management System")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API is working"}

@app.get("/check-db")
def check_db(db: Session = Depends(get_db)):
    return {"status": "Database is connected"}
