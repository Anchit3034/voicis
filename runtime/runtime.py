import ctypes
import wave
import os
import webrtcvad
import asyncio
import time

from stt.whisper_engine import(transcribe)
from optimization.token_optimizer import(optimize_prompt,token_count)
from llm.ollama_runtime import(ask_llm)
from tts.speaker import(speak)

CHUNK_SIZE=400
SAMPLE_RATE=16000

MAX_SILENCE_CHUNKS=20

SEGMENT_DIR="segments"

os.makedirs(SEGMENT_DIR,exist_ok=True)

lib=ctypes.CDLL("./audio/libsegmenter.so")

lib.init_audio()

lib.read_audio.argtypes=[
        ctypes.POINTER(ctypes.c_short)
        ]
vad=webrtcvad.Vad(2)
def save_wav(filename,pcm):
    with wave.open(filename,"wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm)
async def runtime_loop():
    buffer=(ctypes.c_short * CHUNK_SIZE )()
    recording=False
    silence_counter=0
    frames=[]
    segment_count=0
    while True:
        result=lib.read_audio(buffer)
        if result<=0:
            continue
        pcm_bytes=bytes(buffer)
        is_speech=vad.is_speech(pcm_bytes,SAMPLE_RATE)
        if is_speech:
            if not recording:
                print("\n[System] Speech Started")
                recording=True
                frames=[]
            silence_counter=0
            frames.append(pcm_bytes)
        else:
            if recording:
                silence_counter += 1
                frames.append(pcm_bytes)

                if(silence_counter>MAXSILENCE_CHUNKS):
                    filename=(f"{SEGMENT_DIRS}/"
                              f"segment_"
                              f"{segment_count}.wav")
                    segment_count+=1;
                    audio_data=b"".join(frames)
                    save_wav(filename,audio_data)
                    print(
                            f"[System]Saved: "
                            f"{filename}"
                            )
                    start=time.time()
                    text=transcribe(filename)
                    optimized=optimize_prompt(text)
                    original_tokens=(token_count(optimized))
                    print(f"[User] {text}")
                    print(f"[OPTIMIZED] "
                          f"[optimized]"
                          )
                    print(f"[TOKENS] "
                          f"{original_tokens}"
                          f"-> "
                          f"{reduced_tokens}")
                    response=ask_llm(optimized)
                    latency=(time.time()-start)
                    print(f"[AI] {response} ")
                    print(f"[LATENCY] "
                          f"{latency:.2f}s"
                          )
                    speak(response)
                    recording=False
                    silence_counter=0
                    frames=[]
        await asyncio.sleep(0)
asyncio.run(runtime_loop())





    

