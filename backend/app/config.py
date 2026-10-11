import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_NAME = "stethoscope-sound-analyzer"

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./stethoscope.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

API_PREFIX = "/api/v1"

if "postgres" in DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    DATABASE_URL = DATABASE_URL
