import subprocess

PIPER_PATH = (
    "/home/anchit-jain/.local/bin/piper"
)

MODEL_PATH = (
    "./piper/"
    "en_US-lessac-medium.onnx"
)

current_piper = None
current_aplay = None

def stop_tts():

    global current_piper
    global current_aplay

    if current_piper:

        current_piper.kill()

        current_piper = None

    if current_aplay:

        current_aplay.kill()

        current_aplay = None

def speak_stream(text):

    global current_piper
    global current_aplay

    # =====================
    # PIPER PROCESS
    # =====================

    current_piper = subprocess.Popen(
        [
            PIPER_PATH,
            "--model",
            MODEL_PATH,
            "--output_raw"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    # =====================
    # AUDIO PLAYBACK PIPE
    # =====================

    current_aplay = subprocess.Popen(
        [
            "aplay",
            "-r",
            "22050",
            "-f",
            "S16_LE",
            "-t",
            "raw"
        ],
        stdin=current_piper.stdout
    )

    # =====================
    # SEND TEXT
    # =====================

    current_piper.stdin.write(
        text.encode()
    )

    current_piper.stdin.close()

    current_aplay.wait()

    current_piper = None
    current_aplay = None
