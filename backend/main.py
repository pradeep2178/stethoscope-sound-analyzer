from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import API_PREFIX
from app.db import Base, engine, get_db
from app.models import User
from app.routes.auth import router as auth_router
from app.routes.sound import router as sound_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stethoscope Sound Analyzer", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Stethoscope Sound Analyzer API"}


@app.get("/")
def root():
    return {"project": "Stethoscope Sound Analyzer", "status": "running"}


app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(sound_router, prefix=API_PREFIX)
