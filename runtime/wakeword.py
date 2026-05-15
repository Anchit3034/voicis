from openwakeword.model import Model

model=Model()

WAKE_THRESHOLD=0.5

def detect_wakeword(audio_chunk):
    prediction=model.predict(audio_chunk)
    for value in prediction.values():
        if value > WAKE_THRESHOLD:
            return True
    return False

