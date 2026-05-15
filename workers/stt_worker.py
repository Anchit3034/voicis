

import traceback
import time

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
    transcribe_stream
)

from runtime.logger import (
    debug,
    info,
    error
)

def stt_loop():

    while True:

        try:

            pcm_audio = audio_queue.get()

            text = transcribe_stream(
                pcm_audio
            )

            if not text.strip():

                continue

            info(
                f"TRANSCRIPT: {text}"
            )

            stt_queue.put(
                text
            )

            event_queue.put(
                Event.TRANSCRIPTION_READY
            )

            event_bus.put(
                RuntimeMessage(
                    MessageType.TRANSCRIPTION,
                    text
                )
            )

        except Exception:

            error(
                "STT WORKER CRASH"
            )

            traceback.print_exc()

            time.sleep(1)
