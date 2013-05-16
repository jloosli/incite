import threading
import time
from gps import *


class GpsPoller(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None

    def get_current_value(self):
        return self.current_value

    def run(self):
        try:
            while True:
                self.current_value = self.session.next()
        except StopIteration:
            pass


def main():
    gpsp = GpsPoller()
    gpsp.run()
    while 1:
        print gpsp.get_current_value()
        time.sleep(1)

if __name__ == '__main__':
    main()
