import queue
def clear_queue(q):

    while not q.empty():

        try:

            q.get_nowait()

        except:

            break
audio_queue = queue.Queue(maxsize=2)

stt_queue = queue.Queue(maxsize=2)

llm_queue = queue.Queue(maxsize=2)

tts_queue = queue.Queue(maxsize=2)

event_queue = queue.Queue(maxsize=2)
