import subprocess
import tempfile
import os

PIPER_PATH = (
    "./piper/piper"
)

MODEL_PATH = (
    "./piper/"
    "en_US-lessac-medium.onnx"
)

current_process = None

def stop_tts():

    global current_process

    if current_process:

        current_process.kill()

        current_process = None

def speak_stream(text):

    global current_process

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as tmp:

        wav_path = tmp.name

    piper_cmd = [
        PIPER_PATH,
        "--model",
        MODEL_PATH,
        "--output_file",
        wav_path
    ]

    piper = subprocess.Popen(
        piper_cmd,
        stdin=subprocess.PIPE
    )

    piper.stdin.write(
        text.encode()
    )

    piper.stdin.close()

    piper.wait()

    current_process = subprocess.Popen(
        [
            "aplay",
            wav_path
        ]
    )

    current_process.wait()

    os.remove(wav_path)
