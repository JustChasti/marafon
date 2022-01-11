import threading
import time


class DosThread(threading.Thread):
    def __init__(self, id):
        super(DosThread, self).__init__()
        self.id = id
        self.paused = threading.Event()

    def run(self):
        while not self.paused.is_set():
            time.sleep(1)