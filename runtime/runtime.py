import ctypes
import webrtcvad
import threading
import queue
import time

from stt.whisper_engine import (
    transcribe_pcm
)

from optimization.token_optimizer import (
    optimize_prompt
)

from llm.ollama_runtime import (
    stream_llm
)

from tts.speaker import (
    speak_stream,
    stop_tts
)

# =========================
# CONFIG
# =========================

CHUNK_SIZE = 160

SAMPLE_RATE = 16000

MAX_SILENCE_CHUNKS = 4

# =========================
# LOAD AUDIO ENGINE
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
# GLOBALS
# =========================
tts_queue = queue.Queue()

is_speaking = False
is_generating = False
def tts_worker():

    global is_speaking

    while True:

        text = tts_queue.get()

        if text is None:
            continue

        is_speaking = True

        speak_stream(text)

        is_speaking = False
# =========================
# AI THREAD
# =========================

def ai_worker():

    global is_generating

    while True:

        pcm_audio = task_queue.get()

        is_generating = True

        start = time.time()

        # =====================
        # STT
        # =====================

        text = transcribe_pcm(

            pcm_audio
        )

        optimized = optimize_prompt(
            text
        )

        print(
            f"\n[USER] {optimized}"
        )

        # =====================
        # STREAMING LLM
        # =====================

        response = ""

        sentence_buffer = ""

        for token in stream_llm(optimized):
            print(token, end="", flush=True)

            response += token

            sentence_buffer += token

            if token in [".", "!", "?"]:
                tts_queue.put(sentence_buffer)

                sentence_buffer = ""
        
        is_generating = False

# =========================
# START AI THREAD
# =========================
threading.Thread(
    target=tts_worker,
    daemon=True
).start()
threading.Thread(
    target=ai_worker,
    daemon=True
).start()

# =========================
# MAIN LOOP
# =========================
print(
    "=== STREAMING VOICE AI ==="
)

recording = False

silence_counter = 0

frames = []

while True:
    if is_speaking:
        time.sleep(0.01)
        continue
    result = lib.read_audio(buffer)

    if result <= 0:
        continue

    pcm_bytes = bytes(buffer)

    is_speech = vad.is_speech(
        pcm_bytes,
        SAMPLE_RATE
    )

    # =====================
    # INTERRUPTION
    # =====================
    if is_generating and is_speech:

        print("\n[INTERRUPT]")

        stop_tts()

        is_generating = False

        recording = False

        silence_counter = 0

        frames = []

        continue 
    # =====================
    # SPEECH DETECTION
    # =====================

    if is_speech:

        if not recording:

            print(
                "\n[SYSTEM] "
                "Speech Started"
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

                audio_pcm = b"".join(
                    frames
                )

                task_queue.put(
                    audio_pcm
                )

                recording = False

                silence_counter = 0

                frames = []
