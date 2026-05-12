from runtime.queues import (
    stt_queue,
    llm_queue,
    event_queue
)
from runtime.signals import (
    interrupt_event
)
from runtime.events import Event

from llm.ollama_runtime import (
    stream_llm
)

from optimization.token_optimizer import (
    optimize_prompt
)
import runtime.runtime_flags as flags
def llm_loop():

    while True:

        text = stt_queue.get()

        optimized = optimize_prompt(
            text
        )

        response = ""

        print(
            f"\n[USER] {optimized}"
        )

        for token in stream_llm(optimized):

            if interrupt_event.is_set():

                print(
                    "\n[LLM INTERRUPTED]"
                    )

                break
            print(
                token,
                end="",
                flush=True
            )

            response += token

        print()

        llm_queue.put(response)

        event_queue.put(
            Event.RESPONSE_READY
        )
