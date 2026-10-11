from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class SoundAnalysisRequest(BaseModel):
    file_name: str = "recording.wav"
    notes: Optional[str] = None


class SoundAnalysisResult(BaseModel):
    sound_type: str
    predicted_pathology: str
    confidence: str
    notes: Optional[str] = None
    file_name: str
    created_at: datetime


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    class Config:
        orm_mode = True
