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

        except Exception as e:

            print(e)

        speaking_event.clear()

        stop_tts()
