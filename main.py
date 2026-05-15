import threading
import traceback

from runtime.controller import (
    controller
)

from runtime.queues import (
    event_queue
)

from runtime.scheduler import (
    scheduler_loop
)

from workers.audio_worker import (
    audio_loop
)

from workers.stt_worker import (
    stt_loop
)

from workers.llm_worker import (
    llm_loop
)

from workers.tts_worker import (
    tts_loop
)

# =====================
# SAFE THREAD WRAPPER
# =====================

def run_safe(name, fn):

    def wrapped():

        print(f"[THREAD START] {name}")

        try:

            fn()

        except Exception:

            print(
                f"\\n[THREAD CRASH] {name}"
            )

            traceback.print_exc()

    thread = threading.Thread(
        target=wrapped,
        daemon=True
    )

    thread.start()

# =====================
# START THREADS
# =====================

run_safe(
    "audio_worker",
    audio_loop
)

run_safe(
    "stt_worker",
    stt_loop
)

run_safe(
    "llm_worker",
    llm_loop
)

run_safe(
    "tts_worker",
    tts_loop
)

run_safe(
    "scheduler",
    scheduler_loop
)

print(
    "\\n=== REAL RUNTIME STARTED ===\\n"
)

# =====================
# MAIN EVENT LOOP
# =====================

while True:

    try:

        event = event_queue.get()

        controller.handle_event(
            event
        )

    except Exception:

        print(
            "\\n[MAIN LOOP CRASH]"
        )

        traceback.print_exc()
