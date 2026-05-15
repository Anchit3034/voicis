# ==========================================
# runtime/queues.py
# ==========================================

import queue

audio_queue = queue.Queue(
    maxsize=8
)

stt_queue = queue.Queue(
    maxsize=8
)

tts_queue = queue.Queue(
    maxsize=32
)

event_queue = queue.Queue(
    maxsize=64
)

def clear_queue(q):

    while not q.empty():

        try:

            q.get_nowait()

        except:

            break
