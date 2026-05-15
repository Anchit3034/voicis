# ==========================================
# stt/whisper_engine.py
# ==========================================

import whisper
import numpy as np
import traceback

from runtime.logger import (
    info,
    error
)

DEVICE = "cpu"

info(
    f"WHISPER LOADING ON {DEVICE}"
)

MODEL = whisper.load_model(
    "small.en",
    device=DEVICE
)

info(
    "WHISPER READY"
)

def transcribe_stream(audio_pcm):

    try:

        audio = (
            np.frombuffer(
                audio_pcm,
                dtype=np.int16
            )
            .astype(np.float32)
            / 32768.0
        )

        result = MODEL.transcribe(
            audio,
            fp16=False,
            language="en",
            temperature=0
        )

        text = (
            result["text"]
            .strip()
        )

        return text

    except Exception:

        error(
            "WHISPER ERROR"
        )

        traceback.print_exc()

        return ""
