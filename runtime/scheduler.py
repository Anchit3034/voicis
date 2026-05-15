from runtime.bus import (
    event_bus
)

from runtime.messages import (
    MessageType
)

def scheduler_loop():

    while True:

        msg = event_bus.get()

        print(
            f"[BUS] {msg.type}"
        )

        # future routing logic
