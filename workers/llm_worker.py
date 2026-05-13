from runtime.queues import (
    stt_queue,
    tts_queue
)

from llm.ollama_runtime import (
    stream_llm
)

from optimization.token_optimizer import (
    optimize_prompt
)

from runtime.signals import (
    interrupt_event
)

def llm_loop():

    while True:

        text = stt_queue.get()

        optimized = optimize_prompt(
            text
        )

        print(
            f"\n[USER] {optimized}"
        )

        sentence = ""

        for token in stream_llm(
            optimized
        ):

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

            sentence += token

            # =====================
            # SENTENCE STREAMING
            # =====================

            if token in [".", "!", "?"]:

                try:

                    tts_queue.put_nowait(
                        sentence
                    )

                except:

                    pass

                sentence = ""

        print()
