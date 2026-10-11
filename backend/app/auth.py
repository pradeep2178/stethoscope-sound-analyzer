from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.db import get_db
from app.models import AnalysisRecord
from app.schemas import SoundAnalysisRequest, SoundAnalysisResult
from app.services.audio_service import audio_summary, normalize_audio, read_audio_bytes
from app.services.model_service import classify_with_prototype

router = APIRouter(prefix="/sound", tags=["sound"])


@router.post("/analyze", response_model=SoundAnalysisResult)
async def analyze_sound(
    file: UploadFile = File(...),
    request: SoundAnalysisRequest = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    audio, sample_rate = read_audio_bytes(file.file)
    if audio is None or sample_rate is None:
        raise HTTPException(status_code=400, detail="Could not read uploaded audio file.")

    normalized_audio = normalize_audio(audio)
    summary = audio_summary(normalized_audio, sample_rate)
    result = classify_with_prototype(normalized_audio, sample_rate)

    record = AnalysisRecord(
        user_id=current_user.id,
        file_name=request.file_name if request else file.filename,
        sound_type=result["sound_type"],
        predicted_pathology=result["predicted_pathology"],
        confidence=result["confidence"],
        notes=(request.notes if request else None) or f"duration={summary['duration']}s; rms={summary['rms']}",
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
async def history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    records = db.query(AnalysisRecord).filter(AnalysisRecord.user_id == current_user.id).order_by(AnalysisRecord.created_at.desc()).all()
    return [
        {
            "id": record.id,
            "file_name": record.file_name,
            "sound_type": record.sound_type,
            "predicted_pathology": record.predicted_pathology,
            "confidence": record.confidence,
            "notes": record.notes,
            "created_at": record.created_at.isoformat(),
        }
        for record in records
    ]
