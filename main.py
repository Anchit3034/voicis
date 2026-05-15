

import threading
import traceback
import signal
import sys

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
    audio_loop,
    shutdown_event
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

from tts.speaker import (
    stop_tts
)

from runtime.logger import (
    info,
    error
)

system_running = True

# ==========================================
# SIGNAL HANDLER
# ==========================================

def handle_sigint(sig, frame):

    global system_running

    info(
        "SYSTEM SHUTDOWN"
    )

    system_running = False

    shutdown_event.set()

    stop_tts()

    sys.exit(0)

signal.signal(
    signal.SIGINT,
    handle_sigint
)

# ==========================================
# SAFE THREAD WRAPPER
# ==========================================

def run_safe(name, fn):

    def wrapped():

        try:

            fn()

        except Exception:

            error(
                f"{name} CRASH"
            )

            traceback.print_exc()

    thread = threading.Thread(
        target=wrapped,
        daemon=True
    )

    thread.start()

# ==========================================
# START THREADS
# ==========================================

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

info(
    "REAL RUNTIME STARTED"
)

# ==========================================
# MAIN LOOP
# ==========================================

while system_running:

    try:

        event = event_queue.get(
            timeout=0.5
        )

        print(
            f"[EVENT] {event}"
        )

        controller.handle_event(
            event
        )

    except:

        pass
