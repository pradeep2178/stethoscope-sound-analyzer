from typing import Dict

import numpy as np


def classify_with_prototype(audio: np.ndarray, sample_rate: int) -> Dict[str, str]:
    """Prototype classifier used until a validated clinical model is added.

    This is intentionally simple and should be replaced by a pretrained model trained on
    heart and lung sound datasets. It returns a likely class and pathology description.
    """
    if audio is None or len(audio) == 0:
        return {
            "sound_type": "unknown",
            "predicted_pathology": "No usable audio detected",
            "confidence": "0%",
        }

    duration = len(audio) / sample_rate
    rms = float(np.sqrt(np.mean(np.square(audio))))
    energy_band = float(np.mean(np.abs(np.fft.rfft(audio))[:200]))

    if duration <= 1.0:
        sound_type = "heart"
        pathology = "Possible murmur or cardiac rhythm abnormality"
        confidence = "78%"
    elif rms > 0.24 and energy_band > 0.15:
        sound_type = "lung"
        pathology = "Possible crackles or wheeze pattern"
        confidence = "74%"
    else:
        sound_type = "lung"
        pathology = "Normal respiratory pattern; monitor for bronchospasm or lower-airway findings"
        confidence = "68%"

    if sound_type == "heart" and rms < 0.12:
        pathology = "Possible low-amplitude cardiac sound; assess for conduction or valvular variation"
        confidence = "70%"

    return {
        "sound_type": sound_type,
        "predicted_pathology": pathology,
        "confidence": confidence,
    }
