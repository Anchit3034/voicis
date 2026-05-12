from runtime.queues import (
    audio_queue,
    stt_queue,
    event_queue
)

from runtime.events import Event

from stt.whisper_engine import (
    transcribe_pcm
)

def stt_loop():

    while True:

        pcm_audio = audio_queue.get()

        text = transcribe_pcm(
            pcm_audio
        )

        stt_queue.put(text)

        event_queue.put(
            Event.TRANSCRIPTION_READY
        )
