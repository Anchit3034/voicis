````md
# Voice AI Runtime

A low-level real-time conversational AI runtime built using Python, C shared libraries, Whisper, Ollama, and Piper TTS.

This project focuses on:
- realtime audio pipelines
- event-driven runtime architecture
- streaming AI responses
- interruptible TTS
- low-level systems programming concepts
- multithreaded conversational runtimes

---

# Features

- Real-time microphone capture
- PulseAudio-based audio backend
- Shared library audio engine (`.so`)
- Whisper speech-to-text
- Ollama LLM integration
- Streaming token generation
- Piper TTS
- Interruptible speech synthesis
- Event-driven runtime
- Multithreaded workers
- Queue-based runtime architecture
- Graceful shutdown handling
- Runtime logging system
- Context memory support
- Prompt token optimization

---

# Runtime Architecture

```text
Microphone
    ↓
Audio Worker
    ↓
STT Queue
    ↓
Whisper
    ↓
LLM Queue
    ↓
Ollama Runtime
    ↓
TTS Queue
    ↓
Piper TTS
    ↓
Speaker Output
````

---

# Project Structure

```text
voice_ai/
│
├── audio/
│   ├── voice_segmenter.c
│   └── libsegmenter.so
│
├── runtime/
│   ├── controller.py
│   ├── queues.py
│   ├── logger.py
│   ├── events.py
│   ├── state.py
│   ├── signals.py
│   └── scheduler.py
│
├── workers/
│   ├── audio_worker.py
│   ├── stt_worker.py
│   ├── llm_worker.py
│   └── tts_worker.py
│
├── stt/
│   └── whisper_engine.py
│
├── llm/
│   └── ollama_runtime.py
│
├── tts/
│   └── speaker.py
│
├── optimization/
│   └── token_optimizer.py
│
├── memory/
│   └── context_manager.py
│
├── main.py
└── requirements.txt
```

---

# Technologies Used

## Languages

* Python
* C

## AI Models

* Whisper (`small.en`)
* Ollama (`tinyllama`)
* Piper TTS

## Audio Stack

* PulseAudio
* PCM Streaming

## Concepts

* Multithreading
* Producer-Consumer Queues
* Event-Driven Systems
* Streaming Inference
* Runtime Interruption
* Subprocess Management
* Shared Libraries
* Signal Handling

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Anchit3034/voicis.git
cd voice_ai
```

---

# Create Virtual Environment

```bash
python3 -m venv myenv
source myenv/bin/activate
```

---

# Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# Install System Dependencies

```bash
sudo apt install \
libpulse-dev \
ffmpeg \
python3-pyaudio \
portaudio19-dev
```

---

# Compile Audio Engine

```bash
gcc -shared -fPIC \
audio/voice_segmenter.c \
-o audio/libsegmenter.so \
-lpulse-simple \
-lpulse
```

---

# Setup Ollama

Install Ollama:

[https://ollama.com/](https://ollama.com/)

Pull model:

```bash
ollama pull tinyllama
```

Run server:

```bash
ollama serve
```

---

# Setup Piper

Download Piper:

[https://github.com/rhasspy/piper](https://github.com/rhasspy/piper)

Place:

* `piper`
* `en_US-lessac-medium.onnx`

inside:

```text
piper/
```

---

# Run

```bash
python3 main.py
```

---

# Controls

```text
ENTER  → Start / Stop Recording
q      → Quit Runtime
Ctrl+C → Force Shutdown
```

---

# Current Status

Current runtime supports:

* realtime transcription
* streaming LLM responses
* interruptible TTS
* multithreaded pipeline execution

This is still an experimental runtime and not production-ready.

---

# Future Improvements

* Full duplex conversation
* Better interruption handling
* Streaming Whisper inference
* Adaptive VAD
* Echo cancellation
* GPU scheduling
* WebSocket runtime
* Runtime metrics dashboard
* SIMD audio preprocessing
* RNNoise integration
* Wake-word activation
* Better memory/context handling
* Lower latency streaming

---

# Known Issues

* Whisper latency on CPU
* Audio quality depends heavily on microphone quality
* TTS interruption can still race under heavy load
* PulseAudio introduces some latency
* Runtime not optimized for long sessions yet

---

# Learning Goals

This project was built to explore:

* low-level runtime systems
* realtime AI pipelines
* concurrent architecture
* Linux audio systems
* streaming inference systems
* conversational runtime engineering

---

# License

MIT License

---

# Author

Anchit Jain

---

# Final Note

I vibed coded this.

