import ctypes

import os
import webrtcvad
import threading
import queue
import time

from stt.whisper_engine import (
    transcribe_pcm
)

from optimization.token_optimizer import (
    optimize_prompt,
    token_count
)

from llm.ollama_runtime import (
    stream_llm
)

from tts.speaker import (
    speak
)

# =========================
# CONFIG
# =========================

CHUNK_SIZE = 160

SAMPLE_RATE = 16000

MAX_SILENCE_CHUNKS = 8

SEGMENT_DIR = "segments"

os.makedirs(
    SEGMENT_DIR,
    exist_ok=True
)

# =========================
# LOAD C LIBRARY
# =========================

lib = ctypes.CDLL(
    "./audio/libsegmenter.so"
)

lib.init_audio()

lib.read_audio.argtypes = [
    ctypes.POINTER(ctypes.c_short)
]

# =========================
# WEBRTC VAD
# =========================

vad = webrtcvad.Vad(2)

# =========================
# AUDIO BUFFER
# =========================

buffer = (
    ctypes.c_short * CHUNK_SIZE
)()

# =========================
# TASK QUEUE
# =========================

task_queue = queue.Queue()

# =========================
# AI WORKER
# =========================

def ai_worker():

    while True:

        pcm_audio=task_queue.get()
        start = time.time()

        text = transcribe_pcm(
            pcm_audio
        )

        optimized = optimize_prompt(
            text
        )

        original_tokens = (
            token_count(text)
        )

        reduced_tokens = (
            token_count(optimized)
        )

        print(
            f"\n[USER] {text}"
        )

        print(
            f"[OPTIMIZED] "
            f"{optimized}"
        )

        print(
            f"[TOKENS] "
            f"{original_tokens}"
            f" -> "
            f"{reduced_tokens}"
        )

        response = stream_llm(
            optimized
        )

        latency = (
            time.time() - start
        )

        print(
            f"[AI] {response}"
        )

        print(
            f"[LATENCY] "
            f"{latency:.2f}s"
        )

        speak(response)

# =========================
# START AI THREAD
# =========================

threading.Thread(
    target=ai_worker,
    daemon=True
).start()

# =========================
# MAIN AUDIO LOOP
# =========================

print(
    "=== THREADED VOICE AI ==="
)

recording = False

silence_counter = 0

frames = []

segment_count = 0

while True:

    result = lib.read_audio(buffer)

    if result <= 0:
        continue

    pcm_bytes = bytes(buffer)

    is_speech = vad.is_speech(
        pcm_bytes,
        SAMPLE_RATE
    )

    if is_speech:

        if not recording:

            print(
                "\n[SYSTEM] Speech Started"
            )

            recording = True

            frames = []

        silence_counter = 0

        frames.append(pcm_bytes)

    else:

        if recording:

            silence_counter += 1

            frames.append(pcm_bytes)

            if (
                silence_counter >
                MAX_SILENCE_CHUNKS
            ):

                audio_pcm=b"".join(frames)
                task_queue.put(audio_pcm)
                recording = False

                silence_counter = 0

                frames = []
