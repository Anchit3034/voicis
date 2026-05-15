

import time

from runtime.queues import (
    tts_queue
)

from runtime.signals import (
    interrupt_event,
    speaking_event
)

from tts.speaker import (
    speak_stream,
    stop_tts
)

import runtime.signals as signals

from runtime.logger import (
    info,
    error
)

def tts_loop():

    while True:

        try:

            sentence = tts_queue.get()

            if interrupt_event.is_set():

                continue

            speaking_event.set()

            interrupt_event.clear()

            info(
                "TTS SPEAKING"
            )

            speak_stream(sentence)

            speaking_event.clear()

            signals.last_tts_time = (
                time.time()
            )

            stop_tts()

        except Exception as e:

            error(
                f"TTS ERROR: {e}"
            )
