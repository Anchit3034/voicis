import whisper
import numpy as np

MODEL = whisper.load_model(
    "base"
)

def transcribe_pcm(pcm_bytes):
    audio_np=np.frombuffer(pcm_bytes,dtype=np.int16)
    audio_float=(audio_np.astype(np.float32)/32768)
    result = MODEL.transcribe(audio_float,fp16=False)

    return result["text"].strip()
