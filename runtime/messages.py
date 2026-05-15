from enum import Enum

class MessageType(Enum):

    AUDIO_PCM = 0

    TRANSCRIPTION = 1

    AI_TOKEN = 2

    TTS_SENTENCE = 3

    INTERRUPT = 4

    METRIC = 5
