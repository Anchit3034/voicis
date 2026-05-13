import time
from runtime.queues import (
    llm_queue
)

from runtime.signals import (
    interrupt_event,
    speaking_event
)

from tts.speaker import (
    speak_stream,
    stop_tts
)

def tts_loop():

    while True:

        response = llm_queue.get()

        speaking_event.set()

        interrupt_event.clear()

        try:

            speak_stream(response)
            import runtime.signals as signals
            signals.last_tts_time = time.time()

        except Exception as e:

            print(e)

        speaking_event.clear()

        stop_tts()
