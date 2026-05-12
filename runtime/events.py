from enum import Enum

class Event(Enum):

    SPEECH_STARTED = 0

    SPEECH_FINISHED = 1

    TRANSCRIPTION_READY = 2

    RESPONSE_READY = 3

    INTERRUPT = 4
