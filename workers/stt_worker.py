from runtime.bus import (
    event_bus
)

from runtime.message import (
    RuntimeMessage
)

from runtime.messages import (
    MessageType
)

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
        print("[STT] waiting...")
        pcm_audio = audio_queue.get()
        print("[STT] received audio")
        # =====================
        # DIRECT TRANSCRIPTION
        # =====================
        
        text = transcribe_pcm(
            pcm_audio
        )
        
        if not text.strip():
            continue

        print(
            f"\n[TRANSCRIPT] {text}"
        )

        try:

            stt_queue.put_nowait(
                text
            )

        except:

            pass

        event_queue.put(
            Event.TRANSCRIPTION_READY
        )

        event_bus.put(
            RuntimeMessage(
                MessageType.TRANSCRIPTION,
                text
            )
        )
