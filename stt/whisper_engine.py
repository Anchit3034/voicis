import whisper

MODEL = whisper.load_model(
    "tiny"
)

def transcribe(filename):

    result = MODEL.transcribe(
        filename
    )

    return result["text"].strip()
