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

def tts_loop():

    while True:

        print("[TTS] waiting...")

        sentence = tts_queue.get()

        print("[TTS] speaking...")

        speaking_event.set()

        interrupt_event.clear()

        try:

            speak_stream(sentence)

        except Exception as e:

            print(
                f"[TTS ERROR] {e}"
            )

        signals.last_tts_time = (
            time.time()
        )

        speaking_event.clear()

        stop_tts()
