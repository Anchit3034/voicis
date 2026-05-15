import ctypes
import webrtcvad
import collections
import time

import runtime.signals as signals
from runtime.controller import (
    controller
)

from runtime.state import (
    RuntimeState
)
from runtime.events import Event

from runtime.queues import (
    audio_queue,
    event_queue
)

from runtime.signals import (
    speaking_event,
    interrupt_event
)
MIN_AUDIO_BYTES = 12000
CHUNK_SIZE = 480

SAMPLE_RATE = 16000

MAX_SILENCE_CHUNKS = 12
PREBUFFER_CHUNKS = 12

SPEECH_CONFIRM_CHUNKS = 2

INTERRUPT_CONFIRM_CHUNKS = 4

prebuffer = collections.deque(
    maxlen=PREBUFFER_CHUNKS
)

speech_counter = 0

interrupt_counter = 0

lib = ctypes.CDLL(
    "./audio/libsegmenter.so"
)

lib.init_audio()

lib.read_audio.argtypes = [
    ctypes.POINTER(ctypes.c_short)
]

vad = webrtcvad.Vad(1)

buffer = (
    ctypes.c_short * CHUNK_SIZE
)()


def audio_loop():

    global speech_counter
    global interrupt_counter

    recording = False

    silence_counter = 0

    frames = []

    while True:

        if (
            time.time() -
            signals.last_tts_time
        ) < 0.8:

            continue

        result = lib.read_audio(buffer)

        if result <= 0:
            continue

        
        pcm_bytes = memoryview(buffer).cast("B").tobytes()

# =====================
# ALWAYS DRAIN ALSA
# =====================

        if controller.state not in [RuntimeState.IDLE,
                                    RuntimeState.LISTENING,
                                    RuntimeState.SPEAKING]:
            continue

        prebuffer.append(pcm_bytes)
        is_speech = vad.is_speech(
            pcm_bytes,
            SAMPLE_RATE
        )

        if is_speech:

            if speaking_event.is_set():

                interrupt_counter += 1

                if (
                    interrupt_counter >=
                    INTERRUPT_CONFIRM_CHUNKS
                ):

                    print(
                        "\n[INTERRUPT DETECTED]"
                    )

                    interrupt_event.set()

            speech_counter += 1

             
            if (not recording and speech_counter >= SPEECH_CONFIRM_CHUNKS):


                event_queue.put(
                    Event.SPEECH_STARTED
                )

                recording = True
                frames=[]
                frames.extend(prebuffer)

            silence_counter = 0

            frames.append(pcm_bytes)

        else:
            speech_counter = 0

            if recording:
                print(".", end="", flush=True)

                
                
                frames.append(pcm_bytes)
                
                silence_counter += 1
                if (
                    silence_counter >
                    MAX_SILENCE_CHUNKS
                ):

                    audio_pcm = b"".join(
                        frames
                    )
                    if len(audio_pcm) < MIN_AUDIO_BYTES:
                        recording = False

                        silence_counter = 0

                        frames = []

                        continue
                    try:
                        audio_queue.put_nowait(
                            audio_pcm
                        )
                    except Exception as e:
                        print(f"[Audio queue Error] {e}")

                    event_queue.put(
                        Event.SPEECH_FINISHED
                    )

                    recording = False

                    silence_counter = 0

                    frames = []
