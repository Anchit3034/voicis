# ==========================================
# tts/speaker.py
# ==========================================

import subprocess
import threading
import signal
import os
import time

from runtime.signals import (
    interrupt_event
)

PIPER_PATH = (
    "piper"
)

MODEL_PATH = (
    "./piper/en_US-lessac-medium.onnx"
)

current_piper = None
current_aplay = None

process_lock = threading.Lock()

# ==========================================
# FORCE STOP
# ==========================================

def stop_tts():

    global current_piper
    global current_aplay

    with process_lock:

        # =====================
        # STOP APLAY
        # =====================

        if current_aplay:

            try:

                os.killpg(
                    os.getpgid(
                        current_aplay.pid
                    ),
                    signal.SIGTERM
                )

            except:
                pass

            current_aplay = None

        # =====================
        # STOP PIPER
        # =====================

        if current_piper:

            try:

                os.killpg(
                    os.getpgid(
                        current_piper.pid
                    ),
                    signal.SIGTERM
                )

            except:
                pass

            current_piper = None

# ==========================================
# INTERRUPT WATCHER
# ==========================================

def interrupt_monitor():

    while True:

        if interrupt_event.is_set():

            print(
                "\n[TTS INTERRUPTED]"
            )

            stop_tts()

            break

        time.sleep(0.02)

# ==========================================
# STREAM SPEECH
# ==========================================

def speak_stream(text):

    global current_piper
    global current_aplay

    monitor = threading.Thread(
        target=interrupt_monitor,
        daemon=True
    )

    monitor.start()

    with process_lock:

        # =====================
        # START PIPER
        # =====================

        current_piper = subprocess.Popen(

            [
                PIPER_PATH,
                "--model",
                MODEL_PATH,
                "--output-raw"
            ],

            stdin=subprocess.PIPE,

            stdout=subprocess.PIPE,

            preexec_fn=os.setsid
        )

        # =====================
        # START APLAY
        # =====================

        current_aplay = subprocess.Popen(

            [
                "aplay",
                "-r", "22050",
                "-f", "S16_LE",
                "-t", "raw"
            ],

            stdin=current_piper.stdout,

            preexec_fn=os.setsid
        )

    try:

        current_piper.stdin.write(
            text.encode()
        )

        current_piper.stdin.close()

    except:

        stop_tts()

        return

    # =====================
    # WAIT LOOP
    # =====================

    while True:

        if interrupt_event.is_set():

            stop_tts()

            return

        if current_aplay.poll() is not None:

            break

        time.sleep(0.02)

    stop_tts()
