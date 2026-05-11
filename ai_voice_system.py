import ctypes
import webrtcvad
import wave
import whisper
import numpy as np
import collections
import os
import time

# =========================
# CONFIG
# =========================

CHUNK_SIZE = 480
SAMPLE_RATE = 16000

VAD_MODE = 2

MAX_SILENCE_CHUNKS = 20

SEGMENT_DIR = "segments"

# =========================
# LOAD C LIBRARY
# =========================

lib = ctypes.CDLL("./libsegmenter.so")

lib.init_audio()

lib.read_audio.argtypes = [
    ctypes.POINTER(ctypes.c_short)
]

# =========================
# WEBRTC VAD
# =========================

vad = webrtcvad.Vad(VAD_MODE)

# =========================
# WHISPER
# =========================

print("[SYSTEM] Loading Whisper...")

model = whisper.load_model("base")

print("[SYSTEM] Whisper Ready")

# =========================
# BUFFER
# =========================

audio_buffer = (
    ctypes.c_short * CHUNK_SIZE
)()

recording = False

silence_counter = 0

frames = []

segment_count = 0

os.makedirs(SEGMENT_DIR, exist_ok=True)

# =========================
# SAVE WAV
# =========================

def save_wav(filename, pcm_data):

    with wave.open(filename, "wb") as wf:

        wf.setnchannels(1)

        wf.setsampwidth(2)

        wf.setframerate(SAMPLE_RATE)

        wf.writeframes(pcm_data)

# =========================
# MAIN LOOP
# =========================

while True:

    result = lib.read_audio(audio_buffer)

    if result <= 0:
        continue

    pcm_bytes = bytes(audio_buffer)

    is_speech = vad.is_speech(
        pcm_bytes,
        SAMPLE_RATE
    )

    if is_speech:

        if not recording:

            print("[SYSTEM] Speech Started")

            recording = True

            frames = []

        silence_counter = 0

        frames.append(pcm_bytes)

    else:


        if recording:

            silence_counter += 1

            frames.append(pcm_bytes)

            if silence_counter > MAX_SILENCE_CHUNKS:

                filename = (
                    f"{SEGMENT_DIR}/"
                    f"segment_{segment_count}.wav"
                )

                segment_count += 1

                audio_data = b"".join(frames)

                save_wav(filename, audio_data)

                print(
                    f"[SYSTEM] Saved: {filename}"
                )

                start = time.time()

                result = model.transcribe(
                    filename
                )

                latency = (
                    time.time() - start
                )

                text = result["text"].strip()

                print(
                    f"[STT] {text}"
                )

                print(
                    f"[LATENCY] "
                    f"{latency:.2f}s"
                )

                recording = False

                frames = []

                silence_counter = 0
