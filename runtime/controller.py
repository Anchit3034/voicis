from runtime.state import RuntimeState

from runtime.events import Event

from runtime.queues import (
    event_queue
)

class RuntimeController:

    def __init__(self):

        self.state = RuntimeState.IDLE

    def handle_event(self, event):

        print(
            f"[EVENT] {event}"
        )

        # =====================
        # IDLE
        # =====================

        if self.state == RuntimeState.IDLE:

            if event == Event.SPEECH_STARTED:

                self.state = (
                    RuntimeState.LISTENING
                )

        # =====================
        # LISTENING
        # =====================

        elif self.state == RuntimeState.LISTENING:

            if event == Event.SPEECH_FINISHED:

                self.state = (
                    RuntimeState.PROCESSING
                )

        # =====================
        # PROCESSING
        # =====================

        elif self.state == RuntimeState.PROCESSING:

            if event == Event.RESPONSE_READY:

                self.state = (
                    RuntimeState.SPEAKING
                )

        # =====================
        # SPEAKING
        # =====================

        elif self.state == RuntimeState.SPEAKING:

            if event == Event.INTERRUPT:

                self.state = (
                    RuntimeState.LISTENING
                )

        print(
            f"[STATE] {self.state}"
        )

controller = RuntimeController()
