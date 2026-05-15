import whisper
import numpy as np
import torch
import traceback

DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print(
    f"[WHISPER] Loading on {DEVICE}"
)

MODEL = whisper.load_model(
    "base",
    device=DEVICE
)

print(
    "[WHISPER] Ready"
)

def transcribe_pcm(audio_pcm):

    try:

        audio = (
            np.frombuffer(
                audio_pcm,
                dtype=np.int16
            )
            .astype(np.float32)
            / 32768.0
        )
        print(f"[WHISPER AUDIO BYTES] {len(audio_pcm)}")
        print(
            "[WHISPER] Transcribing..."
        )

        result = MODEL.transcribe(
            audio,
            fp16=False,
            language="en"
        )

        text = (
            result["text"]
            .strip()
        )

        print(
            f"[WHISPER] Done: {text}"
        )
        print(f"[WHISPER MAX AMP] {np.max(np.abs(audio))}")

        return text

    except Exception:

        print(
            "\\n[WHISPER ERROR]"
        )

        traceback.print_exc()

        return ""
