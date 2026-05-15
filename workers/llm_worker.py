

import traceback
import time

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

from runtime.logger import (
    debug,
    info,
    error
)

def llm_loop():

    while True:

        try:

            text = stt_queue.get()

            optimized = optimize_prompt(
                text
            )

            info(
                f"USER: {optimized}"
            )

            sentence = ""

            stream = stream_llm(
                optimized
            )

            for token in stream:

                if interrupt_event.is_set():

                    info(
                        "LLM INTERRUPTED"
                    )

                    break

                print(
                    token,
                    end="",
                    flush=True
                )

                sentence += token

                if (
                    "." in token or
                    "!" in token or
                    "?" in token
                ):

                    tts_queue.put(
                        sentence
                    )

                    sentence = ""

            if sentence.strip():

                tts_queue.put(
                    sentence
                )

            print()

        except Exception:

            error(
                "LLM WORKER CRASH"
            )

            traceback.print_exc()

            time.sleep(1)
