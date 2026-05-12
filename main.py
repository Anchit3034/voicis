import threading

from runtime.controller import (
    controller
)

from runtime.queues import (
    event_queue
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

# =========================
# THREADS
# =========================

threading.Thread(
    target=audio_loop,
    daemon=True
).start()

threading.Thread(
    target=stt_loop,
    daemon=True
).start()

threading.Thread(
    target=llm_loop,
    daemon=True
).start()

threading.Thread(
    target=tts_loop,
    daemon=True
).start()

print(
    "=== REAL RUNTIME STARTED ==="
)

# =========================
# EVENT LOOP
# =========================

while True:

    event = event_queue.get()

    controller.handle_event(
        event
    )
