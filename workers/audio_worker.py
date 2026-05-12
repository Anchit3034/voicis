import ctypes
import webrtcvad

from runtime.events import Event

from runtime.queues import (
    audio_queue,
    event_queue
)

CHUNK_SIZE = 160

SAMPLE_RATE = 16000

MAX_SILENCE_CHUNKS = 4

lib = ctypes.CDLL(
    "./audio/libsegmenter.so"
)

lib.init_audio()

lib.read_audio.argtypes = [
    ctypes.POINTER(ctypes.c_short)
]

vad = webrtcvad.Vad(2)

buffer = (
    ctypes.c_short * CHUNK_SIZE
)()

def audio_loop():

    recording = False

    silence_counter = 0

    frames = []

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

                event_queue.put(
                    Event.SPEECH_STARTED
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

                    audio_queue.put(
                        audio_pcm
                    )

                    event_queue.put(
                        Event.SPEECH_FINISHED
                    )

                    recording = False

                    silence_counter = 0

                    frames = []
