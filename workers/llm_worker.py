# ==========================================
# workers/llm_worker.py
# ==========================================

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

def llm_loop():

    while True:

        try:

            print(
                "[LLM] waiting..."
            )

            text = stt_queue.get()

            print(
                "[LLM] got transcript"
            )

            optimized = optimize_prompt(
                text
            )

            print(
                f"\n[USER] {optimized}"
            )

            sentence = ""

            # =====================
            # STREAM TOKENS
            # =====================

            try:

                stream = stream_llm(
                    optimized
                )

                for token in stream:

                    # =====================
                    # INTERRUPT
                    # =====================

                    if interrupt_event.is_set():

                        print(
                            "\n[LLM INTERRUPTED]"
                        )

                        break

                    # =====================
                    # TOKEN OUTPUT
                    # =====================

                    print(
                        token,
                        end="",
                        flush=True
                    )

                    sentence += token

                    # =====================
                    # SENTENCE DETECT
                    # =====================

                    if (
                        "." in token or
                        "!" in token or
                        "?" in token
                    ):

                        # =====================
                        # BLOCKING PUT
                        # NATURAL BACKPRESSURE
                        # =====================

                        tts_queue.put(
                            sentence
                        )

                        sentence = ""

                # =====================
                # REMAINING TOKENS
                # =====================

                if sentence.strip():

                    tts_queue.put(
                        sentence
                    )

                print("\n")

            except Exception:

                print(
                    "\n[LLM STREAM ERROR]"
                )

                traceback.print_exc()

        except Exception:

            print(
                "\n[LLM WORKER CRASH]"
            )

            traceback.print_exc()

            time.sleep(1)
