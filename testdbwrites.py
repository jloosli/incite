#!/usr/bin/python
# -*- coding: utf8 -*-

import sqlite3
import datetime
import time

conn = sqlite3.connect("data/samples.db")
c = conn.cursor()
while 1:
    dt = datetime.datetime.now()
    c.execute('INSERT INTO samples ("date", "dataset") VALUES (?, ?)', (dt, 1))
    conn.commit()
    print "Added %s" % (dt,)
    time.sleep(.01)
