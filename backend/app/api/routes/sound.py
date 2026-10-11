from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models import AnalysisRecord
from app.schemas import SoundAnalysisResult
from app.services.audio_service import audio_summary, normalize_audio, read_audio_bytes
from app.services.model_service import classify_with_prototype

router = APIRouter(prefix="/sound", tags=["sound"])


@router.post("/analyze", response_model=SoundAnalysisResult)
async def analyze_sound(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    audio, sample_rate = read_audio_bytes(file.file)
    if audio is None:
        raise HTTPException(status_code=400, detail="Unable to read audio file")

    normalized = normalize_audio(audio)
    summary = audio_summary(normalized, sample_rate)
    result = classify_with_prototype(normalized, sample_rate)

    record = AnalysisRecord(
        user_id=current_user.id,
        file_name=file.filename,
        sound_type=result["sound_type"],
        predicted_pathology=result["predicted_pathology"],
        confidence=result["confidence"],
        notes=f"duration={summary['duration']}s;rms={summary['rms']}",
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return SoundAnalysisResult(
        sound_type=result["sound_type"],
        predicted_pathology=result["predicted_pathology"],
        confidence=result["confidence"],
        notes=record.notes,
        file_name=record.file_name,
        created_at=datetime.utcnow(),
    )


@router.get("/history")
async def get_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    records = db.query(AnalysisRecord).filter(AnalysisRecord.user_id == current_user.id).order_by(AnalysisRecord.created_at.desc()).all()
    return records
