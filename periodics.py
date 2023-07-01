import time
import threading

class PeriodicSleeper(threading.Thread):
    def __init__(self, task_function, period):
        super().__init__()
        self.daemon = True #exit this thread when the main one terminates
        self.task_function = task_function
        self.period = period
        self.i = 0
        self.t0 = time.time()
        self.running = True
        self.start()

    def sleep(self):
        self.i += 1
        delta = self.t0 + self.period * self.i - time.time()

        if delta > 0:
            time.sleep(delta)
    
    def run(self):
        self.running = True
        while self.running:
            self.task_function()
            self.sleep()

    def stop(self):
        self.running = False
