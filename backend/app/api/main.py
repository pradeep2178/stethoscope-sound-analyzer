from fastapi import FastAPI

from app.api.routes import auth, sound
from app.config import API_PREFIX
from app.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stethoscope Sound Analyzer", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Stethoscope Sound Analyzer API"}

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(sound.router, prefix=API_PREFIX)
