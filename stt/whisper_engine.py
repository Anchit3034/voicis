import whisper

MODEL=whisper.load_model("base")
def transcribe(filename):
    result=MODEL.transcribe(filename)
    return result["text"].strip()
