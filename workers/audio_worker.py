import ctypes
import webrtcvad
import collections
from runtime.events import Event
from runtime.signals import (
    speaking_event,
    interrupt_event
)
from runtime.queues import (
    audio_queue,
    event_queue
)
from runtime.runtime_flags import (
    interrupt_flag
)
CHUNK_SIZE = 160

SAMPLE_RATE = 16000
speech_counter = 0

SPEECH_CONFIRM_CHUNKS = 3
MAX_SILENCE_CHUNKS = 4
PREBUFFER_CHUNKS=12
prebuffer=collections.deque(maxlen=PREBUFFER_CHUNKS)
lib = ctypes.CDLL(
    "./audio/libsegmenter.so"
)

lib.init_audio()

lib.read_audio.argtypes = [
    ctypes.POINTER(ctypes.c_short)
]
prebuffer.append(pcm_bytes)
vad = webrtcvad.Vad(2)

buffer = (
    ctypes.c_short * CHUNK_SIZE
)()

def audio_loop():

    recording = False

    silence_counter = 0

    frames = list(prebuffer)

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

            speech_counter += 1
    # =====================
    # INTERRUPTION
    # =====================

            if speaking_event.is_set():

                print(
                    "\n[INTERRUPT DETECTED]"
                )

                interrupt_event.set()
            if (not recording and speech_counter >= SPEECH_CONFIRM_CHUNKS):


                event_queue.put(
                    Event.SPEECH_STARTED
                )

                recording = True

                frames = list(prebuffer)

            silence_counter = 0

            frames.append(pcm_bytes)

        else:
            speech_counter = 0

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

                    audio_queue.put(
                        audio_pcm
                    )

                    event_queue.put(
                        Event.SPEECH_FINISHED
                    )

                    recording = False

                    silence_counter = 0

                    frames = list(prebuffer)
