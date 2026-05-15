import time

class Metrics:

    def __init__(self):

        self.start_time = 0

    def start(self):

        self.start_time = time.time()

    def stop(self):

        return (
            time.time()
            - self.start_time
        )

metrics = Metrics()
