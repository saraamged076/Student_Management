from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import time
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, get_db
from app.models import models

# routers
from app.routers.routers import router as auth_router
from app.routers.student import router as student_router

# monitoring
from app.monitoring import metrics

# create tables
Base.metadata.create_all(bind=engine)

# app
app = FastAPI(title="Student Management System")
app = FastAPI(title="Student Management System")
# include routers
app.include_router(auth_router)
app.include_router(student_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# metrics
metrics_data = {
    "total_requests": 0,
    "cache_hits": 0,
    "errors": 0,
    "response_time": 0
}


@app.get("/")
def root():
    return {
        "message": "API is working"
    }


@app.get("/check-db")
def check_db(
    db: Session = Depends(get_db)
):
    return {
        "status": "Database is connected"
    }

@app.get("/metrics")
def get_metrics():

    return {
        "status": "healthy",
        "metrics": metrics_data
    }    
#   
@app.middleware("http")
async def track_requests(request: Request, call_next):

    start_time = time.time()

    metrics_data["total_requests"] += 1

    response = await call_next(request)

    process_time = time.time() - start_time

    metrics_data["response_time"] = round(process_time, 4)

    if response.status_code >= 400:
        metrics_data["errors"] += 1

    return response
    
# Monitoring dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    with open("templates/dashboard.html", "r", encoding="utf-8") as file:
        return file.read()    