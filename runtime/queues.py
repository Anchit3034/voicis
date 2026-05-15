import queue

audio_queue = queue.Queue(maxsize=2)

stt_queue = queue.Queue(maxsize=2)

llm_queue = queue.Queue(maxsize=2)

tts_queue = queue.Queue(maxsize=8)

event_queue = queue.Queue(maxsize=2)
def clear_queue(q):

    while not q.empty():

        try:

            q.get_nowait()

        except:

            break
