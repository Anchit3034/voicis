from enum import Enum

class RuntimeState(Enum):

    IDLE = 0

    LISTENING = 1

    PROCESSING = 2

    SPEAKING = 3
