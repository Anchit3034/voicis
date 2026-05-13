import whisper
import numpy as np
import torch

DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

MODEL = whisper.load_model(
    "base",
    device=DEVICE
)

def transcribe_pcm(audio_pcm):

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
        fp16=True,
        language="en"
    )

    return result["text"].strip()
