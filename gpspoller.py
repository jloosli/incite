#!/usr/bin/python
# -*- coding: utf8 -*-

import threading
import time
from gps import *

class GpsPoller(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.gpsd = gps()
        self.gpsd.stream(WATCH_ENABLE | WATCH_NEWSTYLE)
        self.current_value = {}
        self.running = True

    def get_current_value(self):
        return self.current_value

    def run(self):
        # global gpsd
        while self.running:
            data=self.gpsd.next()
            self.current_value[data['class']] = data



def main():
    gpsp = GpsPoller()
    try:
        gpsp.start()
        while 1:
            val = gpsp.get_current_value()
            if 'TPV' in val:
                print "%s:\n\n%s" % ("TPV",val['TPV'])
                time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False
        gpsp.join()
    print "Done.\nExiting."

if __name__ == '__main__':
    main()
