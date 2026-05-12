from runtime.queues import (
    llm_queue
)

from tts.speaker import (
    speak_stream
)

def tts_loop():

    while True:

        response = llm_queue.get()

        speak_stream(response)
