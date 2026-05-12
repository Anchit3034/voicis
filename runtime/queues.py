import queue

audio_queue = queue.Queue(maxsize=2)

stt_queue = queue.Queue(maxsize=2)

llm_queue = queue.Queue(maxsize=2)

tts_queue = queue.Queue(maxsize=2)

event_queue = queue.Queue(maxsize=2)
