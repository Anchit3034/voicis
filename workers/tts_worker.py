# ==========================================
# workers/tts_worker.py
# ==========================================

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
from runtime.queues import (
    clear_queue,
    tts_queue
)

import time
import runtime.signals as signals

def tts_loop():

    while True:

        print("[TTS] waiting...")

        sentence = tts_queue.get()

        print("[TTS] speaking...")

        speaking_event.set()
        interrupt_event.set()
        # CLEAR OLD SPEECH
        clear_queue(tts_queue)

        time.sleep(0.1)

        interrupt_event.clear()

        try:

            speak_stream(sentence)

        except Exception as e:

            print(
                f"[TTS ERROR] {e}"
            )

        speaking_event.clear()

        signals.last_tts_time = (
            time.time()
        )

        stop_tts()
