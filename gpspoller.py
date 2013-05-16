#!/usr/bin/python
# -*- coding: utf8 -*-

import threading
import time
from gps import *

gpsd = None # Set the global variable


class GpsPoller(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        global gpsd
        gpsd = gps()
        gpsd.stream(WATCH_ENABLE | WATCH_NEWSTYLE)
        self.current_value = None
        self.running = True

    def get_current_value(self):
        return self.current_value

    def run(self):
        global gpsd
        while self.running:
            self.current_value=gpsd.next()


def main():
    gpsp = GpsPoller()
    try:
        gpsp.start()
        while 1:
            print "Getting current Value:"
            print gpsp.get_current_value()
        time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
    print "Done.\nExiting."

def main2():
    session = gps()
    session.stream(WATCH_ENABLE | WATCH_NEWSTYLE)
    while 1:
        try:
            report = session.next()
            print "\n" , report , "\n"
            if report['class'] == 'TPV':
                if hasattr(report, 'time'):
                    print report.time
        except KeyError:
            pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print "GPSD has terminated"

if __name__ == '__main__':
    main()
