from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import API_PREFIX
from app.db import Base, engine
from app.routes import auth as auth_routes
from app.routes import sound as sound_routes

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
    return {"status": "ok", "service": "stethoscope-sound-analyzer"}


app.include_router(auth_routes.router, prefix=API_PREFIX)
app.include_router(sound_routes.router, prefix=API_PREFIX)


@app.get("/")
def root():
    return JSONResponse({"message": "Stethoscope Sound Analyzer API"})
